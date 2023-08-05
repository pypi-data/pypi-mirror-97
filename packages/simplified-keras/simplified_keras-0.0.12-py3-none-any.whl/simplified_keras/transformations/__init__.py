import numpy as np
from tensorflow.keras.layers import BatchNormalization, Activation
from tensorflow.keras.optimizers import Adam
import cv2
from tensorflow.keras import activations


def predictions_to_classes(predictions):
    # TODO add posibility to change dtype
    return np.argmax(predictions, axis=-1)


def one_hot_to_sparse(tensor):
    # TODO add posibility to change dtype
    return np.argmax(tensor, axis=1)


def unfreeze_model(model, optimizer=Adam(learning_rate=1e-5), metrics="acc"):
    for layer in model.layers:
        if not isinstance(layer, BatchNormalization):
            layer.trainable = True

    model.compile(optimizer=optimizer, loss=model.loss, metrics=metrics)


def stretch_histogram(img, color_mode='rgb'):
    if color_mode == 'grayscale':
        return __make_streatching(img)
    elif color_mode == 'rgb':
        lab_img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab_img)
        stretched_l = __make_streatching(l, 6)
        lab_out = cv2.merge((stretched_l, a, b))
        return cv2.cvtColor(lab_out, cv2.COLOR_LAB2RGB)
    else:
        raise ValueError('Not supported color mode', color_mode)


def __make_streatching(img, scale_value=0):
    min_value = img.min()
    max_value = img.max()
    # no need to stretch
    if min_value == 0 and max_value == 255:
        return img

    # 6 - empirical value to prevent spike at 255
    scaler = 255.0 / (max_value - min_value + scale_value)
    out = img - min_value
    out = out * scaler
    out = np.round(out).astype('uint8')
    return out.clip(max=255)


def normalize_histogram_clahe(img, clip_limit=2.0, tile_grid_size=(8, 8), color_mode='rgb'):
    if color_mode == 'grayscale':
        return __normalize_clahe(img, clip_limit, tile_grid_size)
    elif color_mode == 'rgb':
        lab_img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab_img)
        l_normalized = __normalize_clahe(l, clip_limit, tile_grid_size)
        lab_out = cv2.merge((l_normalized, a, b))
        return cv2.cvtColor(lab_out, cv2.COLOR_LAB2RGB)


def __normalize_clahe(img, clip_limit, tile_grid_size):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(img)


def replace_activations(model, activation):
    for layer in model.layers:
        if isinstance(layer, Activation) and hasattr(layer, 'activation'):
            layer.activation = activation
