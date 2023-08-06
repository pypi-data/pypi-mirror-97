import numpy as np

import paddle

with paddle.fluid.dygraph.guard():
    x = np.random.rand(16,4,64,3,3).astype('float32')
    x1 = paddle.fluid.dygraph.to_variable(x)
    x2 = paddle.fluid.dygraph.to_variable(x)

    y1 = paddle.fluid.layers.concat(x1, axis=-2)
    x22 = paddle.fluid.layers.transpose(x2, [0,3,1,2,4])
    y2 = paddle.fluid.layers.reshape(x22, [-1, x22.shape[2], x22.shape[3], x22.shape[4]])
    y2 = paddle.fluid.layers.transpose(y2, [1,2,0,3])
    np.testing.assert_allclose(y1.numpy(), y2.numpy())
    print(y2.shape)