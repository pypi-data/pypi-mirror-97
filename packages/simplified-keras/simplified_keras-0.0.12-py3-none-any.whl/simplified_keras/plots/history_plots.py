import matplotlib.pyplot as plt


def plot_acc_and_loss(history, figsize=(10, 10)):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    fig, (ax1, ax2) = plt.subplots(2, 1)

    epochs = range(len(acc))

    ax1.plot(epochs, acc, label='train acc', linewidth=1)
    ax1.plot(epochs, val_acc, label='validation acc', linewidth=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Accuracy')
    ax1.set_title("Accuracy")

    ax2.plot(epochs, loss, label='train loss', linewidth=1)
    ax2.plot(epochs, val_loss, label='validation loss', linewidth=1)
    ax2.legend()
    ax2.grid()
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Loss')
    ax2.set_title("Loss")

    fig.set_figheight(figsize[0])
    fig.set_figwidth(figsize[1])
    plt.show()
    return fig
