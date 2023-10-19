import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.utils.common import save_json


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def prepare_val_data(self):
        val_ds = tf.keras.utils.image_dataset_from_directory(
            directory=self.config.training_data,
            validation_split=0.2,
            subset="validation",
            seed=42,
            batch_size=self.config.params_batch_size,
            image_size=(self.config.params_image_size[0], self.config.params_image_size[1]))

        self.val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    def evaluate(self):
        self.model = self.load_model(self.config.trained_model_path)
        self.prepare_val_data()
        self.score = self.model.evaluate(self.val_ds)
        self.save_score()

    def log_into_mlflow(self):
        mlflow.set_registry_uri(self.config.mlflow_url)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )

            if tracking_url_type_store != "file":
                mlflow.keras.log_model(self.model,
                                       "model",
                                       registered_model_name="VGG16Model")

            else:
                mlflow.keras.log_model(self.model, "model")

    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
