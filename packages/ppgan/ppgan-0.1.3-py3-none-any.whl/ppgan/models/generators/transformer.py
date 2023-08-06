# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import math
import paddle
import paddle.nn as nn
import numpy as np

import paddle.fluid as fluid
import paddle.fluid.layers as layers
import paddle.fluid.dygraph as D
from paddle.fluid.dygraph import Embedding, LayerNorm, Linear, Layer, to_variable
from paddle.fluid.dygraph.learning_rate_scheduler import LearningRateDecay
from .builder import GENERATORS


def position_encoding_init(n_position, d_pos_vec):
    """
    Generate the initial values for the sinusoid position encoding table.
    """
    channels = d_pos_vec
    position = np.arange(n_position)
    num_timescales = channels // 2
    log_timescale_increment = (np.log(float(1e4) / float(1)) /
                               (num_timescales - 1))
    inv_timescales = np.exp(
        np.arange(num_timescales)) * -log_timescale_increment
    scaled_time = np.expand_dims(position, 1) * np.expand_dims(
        inv_timescales, 0)
    signal = np.concatenate([np.sin(scaled_time), np.cos(scaled_time)], axis=1)
    signal = np.pad(signal, [[0, 0], [0, np.mod(channels, 2)]], 'constant')
    position_enc = signal
    return position_enc.astype("float32")


class NoamDecay(LearningRateDecay):
    """
    learning rate scheduler
    """
    def __init__(self,
                 d_model,
                 warmup_steps,
                 static_lr=2.0,
                 begin=1,
                 step=1,
                 dtype='float32'):
        super(NoamDecay, self).__init__(begin, step, dtype)
        self.d_model = d_model
        self.warmup_steps = warmup_steps
        self.static_lr = static_lr

    def step(self):
        a = self.create_lr_var(self.step_num**-0.5)
        b = self.create_lr_var((self.warmup_steps**-1.5) * self.step_num)
        lr_value = (self.d_model**-0.5) * layers.elementwise_min(
            a, b) * self.static_lr
        return lr_value


class PrePostProcessLayer(Layer):
    """
    PrePostProcessLayer
    """
    def __init__(self, process_cmd, d_model, dropout_rate):
        super(PrePostProcessLayer, self).__init__()
        self.process_cmd = process_cmd
        self.functors = []
        for cmd in self.process_cmd:
            if cmd == "a":  # add residual connection
                self.functors.append(lambda x, y: x + y if y is not None else x)
            elif cmd == "n":  # add layer normalization
                self.functors.append(
                    self.add_sublayer(
                        "layer_norm_%d" %
                        len(self.sublayers(include_sublayers=False)),
                        LayerNorm(
                            normalized_shape=d_model,
                            param_attr=fluid.ParamAttr(
                                initializer=fluid.initializer.Constant(1.)),
                            bias_attr=fluid.ParamAttr(
                                initializer=fluid.initializer.Constant(0.)))))
            elif cmd == "d":  # add dropout
                self.functors.append(lambda x: layers.dropout(
                    x, dropout_prob=dropout_rate, is_test=False)
                                     if dropout_rate else x)

    def forward(self, x, residual=None):
        for i, cmd in enumerate(self.process_cmd):
            if cmd == "a":
                x = self.functors[i](x, residual)
            else:
                x = self.functors[i](x)
        return x


class MultiHeadAttention(Layer):
    """
    Multi-Head Attention
    """
    def __init__(self, d_key, d_value, d_model, n_head=1, dropout_rate=0.):
        super(MultiHeadAttention, self).__init__()
        self.n_head = n_head
        self.d_key = d_key
        self.d_value = d_value
        self.d_model = d_model
        self.dropout_rate = dropout_rate
        self.q_fc = Linear(input_dim=d_model,
                           output_dim=d_key * n_head,
                           bias_attr=False)
        self.k_fc = Linear(input_dim=d_model,
                           output_dim=d_key * n_head,
                           bias_attr=False)
        self.v_fc = Linear(input_dim=d_model,
                           output_dim=d_value * n_head,
                           bias_attr=False)
        self.proj_fc = Linear(input_dim=d_value * n_head,
                              output_dim=d_model,
                              bias_attr=False)

    def _prepare_qkv(self, queries, keys, values, cache=None):
        if keys is None:  # self-attention
            keys, values = queries, queries
            static_kv = False
        else:  # cross-attention
            static_kv = True

        q = self.q_fc(queries)
        q = layers.reshape(x=q, shape=[0, 0, self.n_head, self.d_key])
        q = layers.transpose(x=q, perm=[0, 2, 1, 3])

        if cache is not None and static_kv and "static_k" in cache:
            # for encoder-decoder attention in inference and has cached
            k = cache["static_k"]
            v = cache["static_v"]
        else:
            k = self.k_fc(keys)
            v = self.v_fc(values)
            k = layers.reshape(x=k, shape=[0, 0, self.n_head, self.d_key])
            k = layers.transpose(x=k, perm=[0, 2, 1, 3])
            v = layers.reshape(x=v, shape=[0, 0, self.n_head, self.d_value])
            v = layers.transpose(x=v, perm=[0, 2, 1, 3])

        if cache is not None:
            if static_kv and not "static_k" in cache:
                # for encoder-decoder attention in inference and has not cached
                cache["static_k"], cache["static_v"] = k, v
            elif not static_kv:
                # for decoder self-attention in inference
                cache_k, cache_v = cache["k"], cache["v"]
                k = layers.concat([cache_k, k], axis=2)
                v = layers.concat([cache_v, v], axis=2)
                cache["k"], cache["v"] = k, v

        return q, k, v

    def forward(self, queries, keys, values, attn_bias, cache=None):
        # compute q ,k ,v
        q, k, v = self._prepare_qkv(queries, keys, values, cache)

        # scale dot product attention
        product = layers.matmul(x=q,
                                y=k,
                                transpose_y=True,
                                alpha=self.d_model**-0.5)
        if attn_bias is not None:
            product += attn_bias
        weights = layers.softmax(product)
        if self.dropout_rate:
            weights = layers.dropout(weights,
                                     dropout_prob=self.dropout_rate,
                                     is_test=False)

        out = layers.matmul(weights, v)

        # combine heads
        out = layers.transpose(out, perm=[0, 2, 1, 3])
        out = layers.reshape(x=out, shape=[0, 0, out.shape[2] * out.shape[3]])

        # project to output
        out = self.proj_fc(out)
        return out


class FFN(Layer):
    """
    Feed-Forward Network
    """
    def __init__(self, d_inner_hid, d_model, dropout_rate):
        super(FFN, self).__init__()
        self.dropout_rate = dropout_rate
        self.fc1 = Linear(input_dim=d_model, output_dim=d_inner_hid, act="relu")
        self.fc2 = Linear(input_dim=d_inner_hid, output_dim=d_model)

    def forward(self, x):
        hidden = self.fc1(x)
        if self.dropout_rate:
            hidden = layers.dropout(hidden,
                                    dropout_prob=self.dropout_rate,
                                    is_test=False)
        out = self.fc2(hidden)
        return out


class EncoderLayer(Layer):
    """
    EncoderLayer
    """
    def __init__(self,
                 n_head,
                 d_key,
                 d_value,
                 d_model,
                 d_inner_hid,
                 prepostprocess_dropout,
                 attention_dropout,
                 relu_dropout,
                 preprocess_cmd="n",
                 postprocess_cmd="da"):

        super(EncoderLayer, self).__init__()

        self.preprocesser1 = PrePostProcessLayer(preprocess_cmd, d_model,
                                                 prepostprocess_dropout)
        self.self_attn = MultiHeadAttention(d_key, d_value, d_model, n_head,
                                            attention_dropout)
        self.postprocesser1 = PrePostProcessLayer(postprocess_cmd, d_model,
                                                  prepostprocess_dropout)

        self.preprocesser2 = PrePostProcessLayer(preprocess_cmd, d_model,
                                                 prepostprocess_dropout)
        self.ffn = FFN(d_inner_hid, d_model, relu_dropout)
        self.postprocesser2 = PrePostProcessLayer(postprocess_cmd, d_model,
                                                  prepostprocess_dropout)

    def forward(self, enc_input, attn_bias):
        attn_output = self.self_attn(self.preprocesser1(enc_input), None, None,
                                     attn_bias)
        attn_output = self.postprocesser1(attn_output, enc_input)

        ffn_output = self.ffn(self.preprocesser2(attn_output))
        ffn_output = self.postprocesser2(ffn_output, attn_output)
        return ffn_output


class Encoder(Layer):
    """
    encoder
    """
    def __init__(self,
                 n_layer,
                 n_head,
                 d_key,
                 d_value,
                 d_model,
                 d_inner_hid,
                 prepostprocess_dropout,
                 attention_dropout,
                 relu_dropout,
                 preprocess_cmd="n",
                 postprocess_cmd="da"):

        super(Encoder, self).__init__()

        self.encoder_layers = list()
        for i in range(n_layer):
            self.encoder_layers.append(
                self.add_sublayer(
                    "layer_%d" % i,
                    EncoderLayer(n_head, d_key, d_value, d_model, d_inner_hid,
                                 prepostprocess_dropout, attention_dropout,
                                 relu_dropout, preprocess_cmd,
                                 postprocess_cmd)))
        self.processer = PrePostProcessLayer(preprocess_cmd, d_model,
                                             prepostprocess_dropout)

    def forward(self, enc_input, attn_bias):
        for encoder_layer in self.encoder_layers:
            enc_output = encoder_layer(enc_input, attn_bias)
            enc_input = enc_output

        return self.processer(enc_output)


# class Embedder(Layer):
#     """
#     Word Embedding + Position Encoding
#     """
#     def __init__(self, vocab_size, emb_dim, bos_idx=0):
#         super(Embedder, self).__init__()

#         self.word_embedder = Embedding(
#             size=[vocab_size, emb_dim],
#             padding_idx=bos_idx,
#             param_attr=fluid.ParamAttr(
#                 initializer=fluid.initializer.Normal(0., emb_dim**-0.5)))

#     def forward(self, word):
#         word_emb = self.word_embedder(word)
#         return word_emb


class WrapEncoder(Layer):
    """
    embedder + encoder
    """
    def __init__(self, patch_size, input_patch_size, feature_dim, n_layer, n_head, d_key,
                 d_value, d_model, d_inner_hid, prepostprocess_dropout,
                 attention_dropout, relu_dropout, preprocess_cmd,
                 postprocess_cmd):
        super(WrapEncoder, self).__init__()

        self.emb_dropout = prepostprocess_dropout
        self.emb_dim = d_model
        patch_num = (patch_size // input_patch_size) ** 2
        patch_dim = feature_dim * (input_patch_size ** 2)
        self.pos_enc = fluid.layers.create_parameter(name="pos_enc", shape=[1, patch_num, patch_dim], dtype='float32')

        # self.word_embedder = word_embedder
        # self.pos_encoder = Embedding(
        #     size=[max_length, self.emb_dim],
        #     param_attr=fluid.ParamAttr(
        #         initializer=fluid.initializer.NumpyArrayInitializer(
        #             position_encoding_init(max_length, self.emb_dim)),
        #         trainable=False))

        self.encoder = Encoder(n_layer, n_head, d_key, d_value, d_model,
                               d_inner_hid, prepostprocess_dropout,
                               attention_dropout, relu_dropout, preprocess_cmd,
                               postprocess_cmd)

    def forward(self, src_word, src_slf_attn_bias):
        # word_emb = self.word_embedder(src_word)
        # word_emb = layers.scale(x=word_emb, scale=self.emb_dim**0.5)
        # pos_enc = self.pos_encoder(src_pos)
        # pos_enc.stop_gradient = True
        emb = src_word + self.pos_enc[:, :]
        # x += self.pos_embedding[:, :(n + 1)]
        enc_input = layers.dropout(emb,
                                   dropout_prob=self.emb_dropout,
                                   is_test=False) if self.emb_dropout else emb

        enc_output = self.encoder(enc_input, src_slf_attn_bias)
        return enc_output


class DecoderLayer(Layer):
    """
    decoder
    """
    def __init__(self,
                 n_head,
                 d_key,
                 d_value,
                 d_model,
                 d_inner_hid,
                 prepostprocess_dropout,
                 attention_dropout,
                 relu_dropout,
                 preprocess_cmd="n",
                 postprocess_cmd="da"):
        super(DecoderLayer, self).__init__()

        self.preprocesser1 = PrePostProcessLayer(preprocess_cmd, d_model,
                                                 prepostprocess_dropout)
        self.self_attn = MultiHeadAttention(d_key, d_value, d_model, n_head,
                                            attention_dropout)
        self.postprocesser1 = PrePostProcessLayer(postprocess_cmd, d_model,
                                                  prepostprocess_dropout)

        self.preprocesser2 = PrePostProcessLayer(preprocess_cmd, d_model,
                                                 prepostprocess_dropout)
        self.cross_attn = MultiHeadAttention(d_key, d_value, d_model, n_head,
                                             attention_dropout)
        self.postprocesser2 = PrePostProcessLayer(postprocess_cmd, d_model,
                                                  prepostprocess_dropout)

        self.preprocesser3 = PrePostProcessLayer(preprocess_cmd, d_model,
                                                 prepostprocess_dropout)
        self.ffn = FFN(d_inner_hid, d_model, relu_dropout)
        self.postprocesser3 = PrePostProcessLayer(postprocess_cmd, d_model,
                                                  prepostprocess_dropout)

    def forward(self,
                dec_input,
                enc_output,
                self_attn_bias,
                cross_attn_bias,
                cache=None):
        self_attn_output = self.self_attn(self.preprocesser1(dec_input), None,
                                          None, self_attn_bias, cache)
        self_attn_output = self.postprocesser1(self_attn_output, dec_input)

        cross_attn_output = self.cross_attn(
            self.preprocesser2(self_attn_output), enc_output, enc_output,
            cross_attn_bias, cache)
        cross_attn_output = self.postprocesser2(cross_attn_output,
                                                self_attn_output)

        ffn_output = self.ffn(self.preprocesser3(cross_attn_output))
        ffn_output = self.postprocesser3(ffn_output, cross_attn_output)

        return ffn_output


class Decoder(Layer):
    """
    decoder
    """
    def __init__(self, n_layer, n_head, d_key, d_value, d_model, d_inner_hid,
                 prepostprocess_dropout, attention_dropout, relu_dropout,
                 preprocess_cmd, postprocess_cmd):
        super(Decoder, self).__init__()

        self.decoder_layers = list()
        for i in range(n_layer):
            self.decoder_layers.append(
                self.add_sublayer(
                    "layer_%d" % i,
                    DecoderLayer(n_head, d_key, d_value, d_model, d_inner_hid,
                                 prepostprocess_dropout, attention_dropout,
                                 relu_dropout, preprocess_cmd,
                                 postprocess_cmd)))
        self.processer = PrePostProcessLayer(preprocess_cmd, d_model,
                                             prepostprocess_dropout)

    def forward(self,
                dec_input,
                enc_output,
                self_attn_bias,
                cross_attn_bias,
                caches=None):
        for i, decoder_layer in enumerate(self.decoder_layers):
            dec_output = decoder_layer(dec_input, enc_output, self_attn_bias,
                                       cross_attn_bias,
                                       None if caches is None else caches[i])
            dec_input = dec_output

        return self.processer(dec_output)


class WrapDecoder(Layer):
    """
    embedder + decoder
    """
    def __init__(self, n_layer, n_head, d_key,
                 d_value, d_model, d_inner_hid, prepostprocess_dropout,
                 attention_dropout, relu_dropout, preprocess_cmd,
                 postprocess_cmd):
                #  postprocess_cmd, share_input_output_embed, word_embedder):
        super(WrapDecoder, self).__init__()

        self.emb_dropout = prepostprocess_dropout
        self.emb_dim = d_model
        # self.word_embedder = word_embedder
        # self.pos_encoder = Embedding(
        #     size=[max_length, self.emb_dim],
        #     param_attr=fluid.ParamAttr(
        #         initializer=fluid.initializer.NumpyArrayInitializer(
        #             position_encoding_init(max_length, self.emb_dim)),
        #         trainable=False))

        self.decoder = Decoder(n_layer, n_head, d_key, d_value, d_model,
                               d_inner_hid, prepostprocess_dropout,
                               attention_dropout, relu_dropout, preprocess_cmd,
                               postprocess_cmd)

        # if share_input_output_embed:
        #     self.linear = lambda x: layers.matmul(x=x,
        #                                           y=self.word_embedder.
        #                                           word_embedder.weight,
        #                                           transpose_y=True)
        # else:
        #     self.linear = Linear(input_dim=d_model,
        #                          output_dim=trg_vocab_size,
        #                          bias_attr=False)

    def forward(self,
                task_embed,
                trg_slf_attn_bias,
                trg_src_attn_bias,
                enc_output,
                caches=None):
        # word_emb = self.word_embedder(trg_word)
        # word_emb = layers.scale(x=word_emb, scale=self.emb_dim**0.5)
        # pos_enc = self.pos_encoder(trg_pos)

        # pos_enc.stop_gradient = True
        # emb = word_emb + pos_enc
        dec_input = layers.dropout(task_embed,
                                   dropout_prob=self.emb_dropout,
                                   is_test=False) if self.emb_dropout else emb
        dec_output = self.decoder(dec_input, enc_output, trg_slf_attn_bias,
                                  trg_src_attn_bias, caches)
        # dec_output = layers.reshape(
        #     dec_output,
        #     shape=[-1, dec_output.shape[-1]],
        # )
        # logits = self.linear(dec_output)
        # return logits
        return dec_output


@GENERATORS.register()
class Transformer(Layer):
    """
    model
    """
    def __init__(self,
                 batch_size=4,
                 patch_size=48,
                 input_patch_size=3,
                 feature_dim=64,
                 max_length=256,
                 n_layer=12,
                 n_head=8,
                 d_key=64,
                 d_value=64,
                 d_model=3*3*64,
                 d_inner_hid=2048,
                 prepostprocess_dropout=0.1,
                 attention_dropout=0.1,
                 relu_dropout=0.1,
                 # preprocess_cmd="n",
                 preprocess_cmd="",
                 postprocess_cmd="da",
                #  weight_sharing=True,
                 bos_id=0,
                 eos_id=1):
        super(Transformer, self).__init__()
        # src_word_embedder = Embedder(vocab_size=src_vocab_size,
        #                              emb_dim=d_model,
        #                              bos_idx=bos_id)

        patch_num = (patch_size // input_patch_size) ** 2
        patch_dim = feature_dim * (input_patch_size ** 2)

        self.head = LowLevelHead(3, 64, input_patch_size=input_patch_size)
        self.tail = LowLevelTail(64, 3, input_patch_size=input_patch_size, patch_per_edge=patch_size//input_patch_size)

        self.task_embed = fluid.layers.create_parameter(name="task_embed", shape=[batch_size, patch_num, patch_dim], dtype='float32')

        self.encoder = WrapEncoder(patch_size, input_patch_size, feature_dim, n_layer, n_head,
                                   d_key, d_value, d_model, d_inner_hid,
                                   prepostprocess_dropout, attention_dropout,
                                   relu_dropout, preprocess_cmd,
                                   postprocess_cmd)
                                #    postprocess_cmd, src_word_embedder)
        # if weight_sharing:
        #     assert src_vocab_size == trg_vocab_size, (
        #         "Vocabularies in source and target should be same for weight sharing."
        #     )
        #     trg_word_embedder = src_word_embedder
        # else:
        #     trg_word_embedder = Embedder(vocab_size=trg_vocab_size,
        #                                  emb_dim=d_model,
        #                                  bos_idx=bos_id)
        self.decoder = WrapDecoder(n_layer, n_head,
                                   d_key, d_value, d_model, d_inner_hid,
                                   prepostprocess_dropout, attention_dropout,
                                   relu_dropout, preprocess_cmd,
                                   postprocess_cmd)

        # self.trg_vocab_size = trg_vocab_size
        self.n_layer = n_layer
        self.n_head = n_head
        self.d_key = d_key
        self.d_value = d_value

    def forward(self, src_word, src_slf_attn_bias=None, 
                trg_slf_attn_bias=None, trg_src_attn_bias=None):

        features = self.head(src_word)

        enc_output = self.encoder(features, src_slf_attn_bias)
        predict = self.decoder(self.task_embed, trg_slf_attn_bias,
                               trg_src_attn_bias, enc_output)

        output = self.tail(predict)
        return output

class ResBlock(D.Layer):
    def __init__(self, in_channel=64, out_channel=64, kernel_size=5, stride=1, padding=2):
        super(ResBlock, self).__init__()
        self.conv1 = D.Conv2D(in_channel, out_channel, kernel_size, stride, padding)
        self.conv2 = D.Conv2D(out_channel, out_channel, kernel_size, stride, padding)

    def forward(self, data):
        features = self.conv1(data)
        features = self.conv2(features)
        return features + data

class LowLevelHead(D.Layer):
    def __init__(self, in_channel=3, out_channel=64, input_patch_size=3):
        super(LowLevelHead, self).__init__()
        self.input_patch_size = input_patch_size
        self.conv1 = D.Conv2D(in_channel, out_channel, 3, 1, 1)
        self.ResBlock1 = ResBlock(out_channel, out_channel, 5, 1, 2)
        self.ResBlock2 = ResBlock(out_channel, out_channel, 5, 1, 2)

    def _img2words(self, img):
        words = []
        # for i in range(img.shape[2]//patch_size):
        #     for j in range(img.shape[3]//patch_size):
        #         words.append(img[:, i * patch_size: (i + 1) * patch_size + patch_size, j * patch_size : (j + 1) * patch_size + patch_size]
        #                                                       .view(1, img.shape[0], -1, patch_size*patch_size*channels))

        for i in range(img.shape[2]//self.input_patch_size):
            for j in range(img.shape[3]//self.input_patch_size):
                words.append(layers.reshape(layers.crop_tensor(img, 
                                        shape=[img.shape[0], img.shape[1], self.input_patch_size, self.input_patch_size], 
                                        offsets=[0, 0, i * self.input_patch_size, j * self.input_patch_size]),
                                    shape=[img.shape[0], 1, -1])
                            )
        # words = layers.reshape(words, shape=[batch_size, patch_num, -1])
        out = layers.concat(words, axis=1)

        return out

    def forward(self, data):
        features = self.conv1(data)
        features = self.ResBlock1(features)
        features = self.ResBlock2(features)

        features = self._img2words(features)
        return features

def default_conv(in_channels, out_channels, kernel_size, bias=True):
    return nn.Conv2D(
        in_channels, out_channels, kernel_size,
        padding=(kernel_size//2), bias_attr=bias)

class Upsampler(nn.Sequential):
    def __init__(self, scale, n_feats, conv=default_conv, bn=False, act=False, bias=True):
        m = []
        if (scale & (scale - 1)) == 0:    # Is scale = 2^n?
            for _ in range(int(math.log(scale, 2))):
                m.append(conv(n_feats, 4 * n_feats, 3, bias))
                m.append(nn.PixelShuffle(2))
                if bn: m.append(nn.BatchNorm2D(n_feats))

                if act == 'relu':
                    m.append(nn.ReLU())
                elif act == 'prelu':
                    m.append(nn.PReLU(n_feats))

        elif scale == 3:
            m.append(conv(n_feats, 9 * n_feats, 3, bias))
            m.append(nn.PixelShuffle(3))
            if bn: m.append(nn.BatchNorm2D(n_feats))

            if act == 'relu':
                m.append(nn.ReLU())
            elif act == 'prelu':
                m.append(nn.PReLU(n_feats))
        else:
            raise NotImplementedError

        super(Upsampler, self).__init__(*m)

class LowLevelTail(D.Layer):
    def __init__(self, in_channel=64, out_channel=3, input_patch_size=3, patch_per_edge=16):
        super(LowLevelTail, self).__init__()
        self.up = Upsampler(4, 64)
        self.conv1 = D.Conv2D(in_channel, out_channel, 3, 1, 1)
        self.input_patch_size = input_patch_size
        self.patch_per_edge = patch_per_edge

    def _words2img(self, words):
        patches = layers.reshape(words, shape=[words.shape[0], words.shape[1], -1, self.input_patch_size, self.input_patch_size])
        patches = layers.transpose(patches, perm=[1, 0, 2, 3, 4])
        # print('debug patch:', patches.shape) 
        cols = []
        for i in range(self.patch_per_edge):
            # print('debug patch 1:', patches[i*self.patch_per_edge:(i+1)*self.patch_per_edge].shape)
            # print('debug patch 2:', layers.concat(
                # input=[patches[i*self.patch_per_edge:(i+1)*self.patch_per_edge]], axis=-2).shape)
            tmp = patches[i*self.patch_per_edge:(i+1)*self.patch_per_edge]
            tmp = paddle.fluid.layers.transpose(tmp, [0,3,1,2,4])
            tmp = paddle.fluid.layers.reshape(tmp, [-1, tmp.shape[2], tmp.shape[3], tmp.shape[4]])
            tmp = paddle.fluid.layers.transpose(tmp, [1,2,0,3])
            
            cols.append(tmp)

            # cols.append(layers.concat(
            #     input=patches[i*self.patch_per_edge:(i+1)*self.patch_per_edge], axis=-2))
            # print('debug cols 2:', cols[i].shape)
        img = layers.concat(input=cols, axis=-1)
        # print('debug img:', img.shape, i)
        return img

    def forward(self, data):
        features = self._words2img(data)
        features = self.up(features)
        output = self.conv1(features)
        return output


if __name__ == '__main__':
    import paddle
    from paddle.fluid.dygraph.base import to_variable

    model = Transformer(4)
    # x = np.random.rand(4,3,48,48).astype('float32')
    # x = to_variable(x)
    x = paddle.rand([4, 3, 48, 48])
    y = model(x)
    print(y.shape)
    
    # with fluid.dygraph.guard():
    #     model = Transformer(4)
    #     x = np.random.rand(4,3,48,48).astype('float32')
    #     x = to_variable(x)
    #     # x = paddle.rand([4, 3, 48, 48])
    #     y = model(x)
    #     print(y.shape)