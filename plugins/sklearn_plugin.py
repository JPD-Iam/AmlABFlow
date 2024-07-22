import mlflow.sklearn
import joblib
from .base_plugin import BasePlugin
class SklearnPlugin(BasePlugin):
    def __init__(self):
        self.model=None
    
    def log_model(self,experiment_id, model_path, model_name, description, version, accuracy, model_type):
        with mlflow.start_run(experiment_id=experiment_id) as run:
            mlflow.log_param("model_name", model_name)
            mlflow.log_param("version", version)
            mlflow.log_param("description", description)
            mlflow.log_param("accuracy", accuracy)
            mlflow.log_param("model_type", model_type)

            model = joblib.load(model_path)
            mlflow.sklearn.log_model(model, artifact_path="model")
            mlflow.set_tag("version", version)
            return run.info.run_id
        
    def load_model(self, model_uri):
        self.model = mlflow.sklearn.load_model(model_uri)
        
        
    def predict(self,data):
        return self.model.predict(data)
    
    