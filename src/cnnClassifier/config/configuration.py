import os
from cnnClassifier.constants import *
from cnnClassifier.utils.common import read_yaml, create_directories
from cnnClassifier.entity.config_entity import (DataIngestionConfig,
                                                PrepareBaseModelConfig,
                                                TrainingConfig,
                                                EvaluationConfig)


class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILEPATH,
            params_filepath=PARAMS_FILEPATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config

    def prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        create_directories([config.root_dir])
        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_model_path=Path(config.updated_model_path),
            params_learning_rate=self.params.LEARNING_RATE,
            params_image_size=self.params.IMAGE_SIZE,
            params_classes=self.params.CLASSES,
            params_weights=self.params.WEIGHTS,
            params_include_top=self.params.INCLUDE_TOP
        )

        return prepare_base_model_config

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params

        training_data = os.path.join(
            self.config.data_ingestion.unzip_dir,
            "Chicken-fecal-images"
        )

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path), updated_model_path=Path(prepare_base_model.updated_model_path),
            training_data=training_data,
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_image_size=params.IMAGE_SIZE,
            params_is_augmentation=params.AUGMENTATION
        )

        return training_config
    
    def get_evaluation_config(self) -> EvaluationConfig:
        evaluation_config = EvaluationConfig(
            trained_model_path=Path(self.config.training.trained_model_path),
            training_data=os.path.join(
                self.config.data_ingestion.unzip_dir, "Chicken-fecal-images"),
            mlflow_url="https://dagshub.com/amulyaprasanth/chiicken_disease_classification.mlflow ",
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return evaluation_config
