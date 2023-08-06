from Accuinsight.Lifecycle import keras
from Accuinsight.Lifecycle import tensorflow


class Lifecycle:
    """
    The exposed class to user
    """

    def run_keras(self, tag=None):
        keras.autolog(tag)

    def run_tensorflow(self, tag=None):
        tensorflow.autolog(tag)
