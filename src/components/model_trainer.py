import sys
import importlib
import logging

from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold
)

from sklearn.metrics import (
    f1_score,
    fbeta_score,
    precision_score,
    recall_score,
    accuracy_score,
    classification_report,
    make_scorer
)
from sklearn.pipeline import Pipeline
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import (
    DataPreprocessingArtifact,
    ModelTrainerArtifact
)

from src.exception.exception import CustomException

from src.utils.utils import (
    read_yaml,
    load_numpy_array_data,
    save_artifact,
    load_artifact
)


class ModelTrainer:

    def __init__(
        self,
        config: dict,
        preprocessing_artifact: DataPreprocessingArtifact
    ):

        logging.info(
            "Initializing Model Trainer"
        )

        self.preprocessing_artifact = preprocessing_artifact
        

        self.config = ModelTrainerConfig(
            config=config
        )

        logging.info(
            "Model Trainer initialized successfully"
        )

    # CREATE MODEL FROM YAML
    
    @staticmethod
    def get_class_from_path(class_path: str):

        try:

            module_name, class_name = (
                class_path.rsplit(".", 1)
            )

            module = importlib.import_module(
                module_name
            )

            model_class = getattr(
                module,
                class_name
            )

            return model_class

        except Exception as e:

            logging.exception(
                "Failed to import class: %s",
                class_path
            )

            raise CustomException(
                e,
                sys
            )

    
    # CREATE ALL MODELS
    

    def create_models(
        self,
        model_config: dict
    ):

        try:

            logging.info(
                "Creating models from model.yaml"
            )

            models = {}

            for model_name, config in model_config.items():

                class_path = config["class"]

                init_params = config.get(
                    "init_params",
                    {}
                )

                logging.info(
                    "Creating model: %s",
                    model_name
                )

                logging.info(
                    "Class: %s",
                    class_path
                )

                logging.info(
                    "Initialization parameters: %s",
                    init_params
                )

                model_class = (
                    self.get_class_from_path(
                        class_path
                    )
                )

                model = model_class(
                    **init_params
                )

                models[model_name] = model

            logging.info(
                "Successfully created %d models",
                len(models)
            )

            return models

        except Exception as e:

            logging.exception(
                "Error occurred while creating models"
            )

            raise CustomException(
                e,
                sys
            )

    
    # EVALUATE MODELS
    

    def evaluate_models(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
        models: dict,
        params: dict
    ):

        try:

            logging.info(
                "Starting model evaluation"
            )

            report = {}

            cv = StratifiedKFold(
                n_splits=5,
                shuffle=True,
                random_state=42
            )
            f2_scorer = make_scorer(fbeta_score, beta=2, zero_division=0)
            for model_name, model in models.items():

                logging.info(
                    "========================================"
                )

                logging.info(
                    "Starting model: %s",
                    model_name
                )

                
                # GET HYPERPARAMETERS
                

                model_params = params.get(
                    model_name,
                    {}
                )

                logging.info(
                    "Hyperparameter space for %s: %s",
                    model_name,
                    model_params
                )

                
                # RANDOMIZED SEARCH
                

                search = RandomizedSearchCV(
                    estimator=model,
                    param_distributions=model_params,
                    n_iter=30,
                    scoring=f2_scorer,
                    cv=cv,
                    random_state=42,
                    n_jobs=-1,
                    verbose=1,
                    refit=True
                )

                logging.info(
                    "Running RandomizedSearchCV for %s",
                    model_name
                )

                search.fit(
                    X_train,
                    y_train
                )

                
                # BEST MODEL
                

                best_model = (
                    search.best_estimator_
                )

                logging.info(
                    "Best parameters for %s: %s",
                    model_name,
                    search.best_params_
                )

                logging.info(
                    "Best CV F2 for %s: %.4f",
                    model_name,
                    search.best_score_
                )

                
                # TRAIN PREDICTION
                

                y_train_pred = (
                    best_model.predict(X_train)
                )

               
                # TEST PREDICTION
                

                y_test_pred = (
                    best_model.predict(X_test)
                )

                
                # METRICS
                

                train_f1 = f1_score(
                    y_train,
                    y_train_pred,
                    zero_division=0
                )
                train_f2 = fbeta_score(
                    y_train,
                    y_train_pred,
                    beta=2,
                    zero_division=0
                )
                test_f1 = f1_score(
                    y_test,
                    y_test_pred,
                    zero_division=0
                )

                test_f2 = fbeta_score(
                    y_test,
                    y_test_pred,
                    beta=2,
                    zero_division=0
                )

                test_precision = precision_score(
                    y_test,
                    y_test_pred,
                    zero_division=0
                )

                test_recall = recall_score(
                    y_test,
                    y_test_pred,
                    zero_division=0
                )

                test_accuracy = accuracy_score(
                    y_test,
                    y_test_pred
                )
                
                # LOG RESULTS
                

                logging.info(
                    "%s Train F1: %.4f",
                    model_name,
                    train_f1
                )
                logging.info(
                    "%s Train F2: %.4f",
                    model_name,
                    train_f2
                )
                logging.info(
                    "%s Test F1: %.4f",
                    model_name,
                    test_f1
                )

                logging.info(
                    "%s Test F2: %.4f",
                    model_name,
                    test_f2
                )

                logging.info(
                    "%s Test Precision: %.4f",
                    model_name,
                    test_precision
                )

                logging.info(
                    "%s Test Recall: %.4f",
                    model_name,
                    test_recall
                )

                logging.info(
                    "%s Test Accuracy: %.4f",
                    model_name,
                    test_accuracy
                )

                logging.info(
                    "Classification Report for %s:\n%s",
                    model_name,
                    classification_report(
                        y_test,
                        y_test_pred,
                        zero_division=0
                    )
                )
                
                # STORE RESULTS
                

                report[model_name] = {
                    "model": best_model,
                    "cv_f2": search.best_score_,
                    "train_f1": train_f1,
                    "train_f2": train_f2,
                    "test_f1": test_f1,
                    "test_f2": test_f2,
                    "precision": test_precision,
                    "recall": test_recall,
                    "accuracy": test_accuracy,
                    "best_params": search.best_params_
}
                logging.info(
                    "Completed model: %s",
                    model_name
                )

            logging.info(
                "All models evaluated successfully"
            )

            return report

        except Exception as e:

            logging.exception(
                "Error occurred during model evaluation"
            )

            raise CustomException(
                e,
                sys
            )

    
    # START TRAINING
    

    def start_training(
        self
    ) -> ModelTrainerArtifact:

        try:

            logging.info(
                "Starting model training pipeline"
            )

            
            # LOAD YAML
            

            data = read_yaml(
                file_path=(
                    self.config.model_yaml_file_path
                )
            )

            model_config = data["models"]

            params = data["params"]

            logging.info(
                "Model YAML loaded successfully"
            )

            
            # CREATE MODELS
            

            models = self.create_models(
                model_config=model_config
            )

            
            # LOAD TRAINING DATA
            

            logging.info(
                "Loading training data"
            )

            X_train = load_numpy_array_data(
                self.preprocessing_artifact
                .X_train_file_path
            )

            y_train = load_numpy_array_data(
                self.preprocessing_artifact
                .y_train_file_path
            )

            X_test = load_numpy_array_data(
                self.preprocessing_artifact
                .X_test_file_path
            )

            y_test = load_numpy_array_data(
                self.preprocessing_artifact
                .y_test_file_path
            )

            logging.info(
                "X_train shape: %s",
                X_train.shape
            )

            logging.info(
                "y_train shape: %s",
                y_train.shape
            )

            logging.info(
                "X_test shape: %s",
                X_test.shape
            )

            logging.info(
                "y_test shape: %s",
                y_test.shape
            )

            
            # EVALUATE MODELS
           

            model_report = self.evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                params=params
            )

            
            # FIND BEST MODEL
            

            best_model_name = max(
                model_report,
                key=lambda name:
                model_report[name]["cv_f2"]
            )

            best_model = (
                model_report[
                    best_model_name
                ]["model"]
            )

            best_model_score = (
                model_report[
                    best_model_name
                ]["cv_f2"]
            )

            logging.info(
                "========================================"
            )

            logging.info(
                "Best model based on CV F2: %s",
                best_model_name
            )

            logging.info(
                "Best model CV F2: %.4f",
                best_model_score
            )
            logging.info(
                "Best model Test F2: %.4f",
                model_report[
                    best_model_name
                ]["test_f2"]
            )

            logging.info(
                "Best model Test Precision: %.4f",
                model_report[
                    best_model_name
                ]["precision"]
            )

            logging.info(
                "Best model Test Recall: %.4f",
                model_report[
                    best_model_name
                ]["recall"]
            )

            logging.info(
                "Best model Test F1: %.4f",
                model_report[
                    best_model_name
                ]["test_f1"]
            )
            logging.info(
                "Best model parameters: %s",
                model_report[
                    best_model_name
                ]["best_params"]
            )
            # SAVE BEST MODEL
            

            model_path = (
                self.config.model_dir
                / "model.pkl"
            )

            save_artifact(
                artifact=best_model,
                path=model_path
            )

            logging.info(
                "Best model saved to: %s",
                model_path
            )

            #SAVE BOTH PREPROCESSOR AND MODEL INTO ONE MODEL:FINAL MODEL
            preprocessr= load_artifact(path= self.preprocessing_artifact.preprocessor_file_path)
            final_model = Pipeline([
                ("preprocessor", preprocessr),
                ("best_model", best_model)
            ])
            final_model_path = self.config.model_dir / "final_model.pkl"
            save_artifact(artifact= final_model, path= final_model_path)
            logging.info(
                            "final model saved to: %s",
                            final_model_path
                        )

            
            # CREATE ARTIFACT
            

            model_trainer_artifact = (
                ModelTrainerArtifact(
                    trained_model_file_path=str(
                        model_path
                    ),
                    model_name=best_model_name,
                    model_score=best_model_score,
                    final_model_file_path= str(final_model_path)
                )
            )

            logging.info(
                "ModelTrainerArtifact created successfully"
            )

            logging.info(
                "Model training completed successfully"
            )

            return model_trainer_artifact

        except Exception as e:

            logging.exception(
                "Error occurred during model training"
            )

            raise CustomException(
                e,
                sys
            )