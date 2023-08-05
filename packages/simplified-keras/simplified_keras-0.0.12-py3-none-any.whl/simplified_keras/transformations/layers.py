from tensorflow.keras.layers import Layer
from tensorflow.image import random_saturation, random_hue, random_brightness
# import random
# import numpy as np


class RandomSaturation(Layer):
    def __init__(self, lower, upper, **kwargs):
        super().__init__(**kwargs)
        self.lower = lower
        self.upper = upper

    def call(self, x, training=None, **kwargs):
        if not training:
            return x
        return random_saturation(x, self.lower, self.upper)


class RandomHue(Layer):
    def __init__(self, max_delta, **kwargs):
        super().__init__(**kwargs)
        self.max_delta = max_delta

    def call(self, x, training=None, **kwargs):
        if not training:
            return x
        return random_hue(x, self.max_delta)


class RandomBrightness(Layer):
    def __init__(self, max_delta, **kwargs):
        super().__init__(**kwargs)
        self.max_delta = max_delta

    def call(self, x, training=None, **kwargs):
        if not training:
            return x
        return random_brightness(x, self.max_delta)


# class RandomGaussianNoise(tf.keras.layers.Layer):
#     def __init__(self, max_stddev, **kwargs):
#         super().__init__(**kwargs)
#         self.max_stddev = max_stddev
#
#     def call(self, x, training=None, **kwargs):
#         std_dev = random.uniform(0, self.max_stddev)
#         noise = np.random.normal(size=self.input_shape, scale=std_dev)
#         x += noise
#         return x
