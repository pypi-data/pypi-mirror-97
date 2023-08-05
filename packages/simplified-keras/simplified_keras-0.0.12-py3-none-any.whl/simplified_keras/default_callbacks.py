import tensorflow.keras.callbacks as clb


def get_default_callbacks(model_path, monitor='val_acc', base_patience=3, lr_reduce_factor=0.5, min_lr=1e-7, verbose=1):
    return [
        clb.ReduceLROnPlateau(monitor=monitor, factor=lr_reduce_factor, min_lr=min_lr, patience=base_patience, verbose=verbose),
        clb.EarlyStopping(monitor=monitor, patience=(2 * base_patience + 1), verbose=verbose),
        clb.ModelCheckpoint(monitor=monitor, filepath=model_path, save_best_only=True, verbose=verbose)
    ]


def restore_callbacks(callbacks, best_monitor_value):
    for callback in callbacks:
        if isinstance(callback, (clb.ModelCheckpoint, clb.ReduceLROnPlateau)):
            if 'loss' in callback.monitor and best_monitor_value <= 0:
                raise ValueError(f'{callback.monitor} should be > 0')

            if 'acc' in callback.monitor and not 0 < best_monitor_value < 1:
                raise ValueError(f'{callback.monitor} should be between 0 and 1')
            callback.best = best_monitor_value
