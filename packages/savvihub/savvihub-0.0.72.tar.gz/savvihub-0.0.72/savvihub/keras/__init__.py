import keras

from savvihub import log


class SavviHubCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        log(
            step=epoch,
            row={'loss': logs.get('loss'), 'accuracy': logs.get('accuracy')}
        )
        print(f'epoch: {epoch}, logs: {logs}')
