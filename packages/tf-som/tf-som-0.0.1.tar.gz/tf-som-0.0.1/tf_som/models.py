import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as tfkl

from .layers import LCA, Conv2DLCA

def ConvNet(input_shape = (64, 64, 3), num_colors=32, num_filters=128, lr_w=1e-3, backpropagatable=True, name=None):
    assert input_shape[0] >= 16 and input_shape[1] >= 16, 'after max pooling (4,4) twice, tensors smaller than (16,' \
                                                          '16) are too small to extract spatial data from. '
    return keras.Sequential([
        #keras.layers.Input(input_shape),
        LCA(N_w=num_colors, lr_w=lr_w, backpropagatable=backpropagatable),
        tfkl.MaxPool2D((4,4)),
        Conv2DLCA(filters=num_filters, kernel_size=(3,3), strides=1, lr_w=lr_w, backpropagatable=backpropagatable),
        tfkl.MaxPool2D((4,4)),
        Conv2DLCA(filters=num_filters, kernel_size=(3,3), strides=1, lr_w=lr_w, backpropagatable=backpropagatable),
        keras.layers.Lambda(lambda x: tf.reduce_sum(x, axis=[-3, -2]))
    ], name=name)