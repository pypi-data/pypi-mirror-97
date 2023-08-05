import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


def plot_predictions_with_img(i, predictions, labels, img, named_labels=None, grayscale=False, figsize=(10, 5)):
    predictions, labels, img = predictions[i], labels[i], img[i]
    predicted_label = np.argmax(predictions)
    true_value = np.argmax(labels)

    if not named_labels:
        named_labels = np.arange(len(labels))

    fig = plt.figure(figsize=figsize)
    plt.subplot(1, 2, 1)

    plt.yticks(np.arange(len(labels)), named_labels)
    thisplot = plt.barh(range(len(predictions)), predictions, color="gray")
    thisplot[predicted_label].set_color('r')
    thisplot[true_value].set_color('g')

    plt.subplot(1, 2, 2)

    if grayscale:
        plt.imshow(np.squeeze(img), cmap='gray')
    else:
        plt.imshow(img)
    plt.xlabel("Predicted: {} {:2.0f}% (Real: {})".format(named_labels[predicted_label], 100 * np.max(predictions),
                                                          named_labels[true_value]))
    plt.show()
    return fig


def plot_img_with_histogram(img, figsize=(10, 5), brightness_range=(0, 255), color_mode='rgb'):
    if color_mode == 'rgb':
        return __plot_rgb_img_with_histogram(img, figsize, brightness_range)
    elif color_mode == 'grayscale':
        return __plot_gray_img_with_histogram(img, figsize, brightness_range)
    else:
        raise ValueError("Unsupported color mode", color_mode)


def __plot_gray_img_with_histogram(img, figsize, brightness_range):
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])

    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    ax1.plot(cdf_normalized, color='b')
    ax1.hist(img.flatten(), 256, [0, 256], color='r')
    ax1.set_xlim([0, 256])

    vmin, vmax = brightness_range
    ax2.imshow(img, cmap='gray', vmin=vmin, vmax=vmax)
    return fig


def __plot_rgb_img_with_histogram(img, figsize, brightness_range):
    flatten_img = np.zeros((3, img.shape[0] * img.shape[1]) )
    for i in range(3):
        flatten_img[i] = img[:, :, i].flatten()

    df = pd.DataFrame(flatten_img.T, columns=['r', 'g', 'b'])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    sns.histplot(data=df, multiple="stack", palette=['red', 'green', 'blue'], ax=ax1)
    ax1.set_xlim([-1, 256])

    vmin, vmax = brightness_range
    ax2.imshow(img, cmap='gray', vmin=vmin, vmax=vmax)
    return fig


def plot_confusion_matrix(cm, labels, figsize=(10, 8), heatmap_options=None):
    heatmap_opt = {'annot': True, 'cmap': plt.cm.Blues}
    if heatmap_options:
        heatmap_opt.update(heatmap_options)

    con_mat_df = pd.DataFrame(cm, index=labels, columns=labels)
    fig = plt.figure(figsize=figsize)
    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True

    if issubclass(cm.dtype.type, np.integer):
        sns.heatmap(con_mat_df, fmt='d', **heatmap_opt)
    else:
        sns.heatmap(con_mat_df, **heatmap_opt)

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    return fig
