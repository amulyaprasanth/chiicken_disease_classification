import tensorflow as tf
from pathlib import Path
from cnnClassifier.entity.config_entity import TrainingConfig


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.updated_model_path
        )

    def prepare_data_for_training(self):
        train_ds = tf.keras.utils.image_dataset_from_directory(
            directory=self.config.training_data,
            validation_split=0.2,
            subset="training",
            seed=42,
            batch_size=self.config.params_batch_size,
            image_size=(
                self.config.params_image_size[0], self.config.params_image_size[1])
        )

        val_ds = tf.keras.utils.image_dataset_from_directory(
            directory=self.config.training_data,
            validation_split=0.2,
            subset="validation",
            seed=42,
            batch_size=self.config.params_batch_size,
            image_size=(self.config.params_image_size[0], self.config.params_image_size[1]))

        if self.config.params_is_augmentation:
            train_aug = tf.keras.Sequential([
                tf.keras.layers.Rescaling(scale=1.0 / 255),
                tf.keras.layers.RandomFlip("horizontal_and_vertical"),
                tf.keras.layers.RandomZoom(
                    height_factor=(-0.05, -0.15),
                    width_factor=(-0.05, -0.15)),
                tf.keras.layers.RandomRotation(0.3)
            ])

            test_aug = tf.keras.Sequential([
                tf.keras.layers.Rescaling(scale=1.0 / 255)
            ])

            self.train_ds = train_ds.map(lambda x, y: (train_aug(x), y),
                                         num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)
            self.val_ds = val_ds.map(lambda x, y: (test_aug(x), y),
                                     num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)

        else:
            self.train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
            self.val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    def train(self):
        self.model.fit(
            self.train_ds,
            epochs=self.config.params_epochs,
            validation_data=self.val_ds,
        )

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
