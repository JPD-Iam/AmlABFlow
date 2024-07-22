import mlflow
from mlflow.tracking import MlflowClient
import joblib
import mlflow.sklearn
from plugins.plugin_manager import PluginManager
from plugins.sklearn_plugin import SklearnPlugin

plugin = SklearnPlugin()



mlflow.set_tracking_uri("http://127.0.0.1:5000")
client=MlflowClient()


    
def create_experiment_if_not_exists(model_name):
    try:
        experiment_id =client.create_experiment(model_name)
    except mlflow.exceptions.MlflowException:
        experiment_id=client.get_experiment_by_name(model_name).experiment_id 
    return experiment_id


def log_model(model_path, model_name, description, version, accuracy, model_type):
    experiment_id = create_experiment_if_not_exists(model_name)
    return plugin.log_model(experiment_id,model_path, model_name, description, version, accuracy, model_type)       
       
def get_model_uri(model_name,version,model_type):
    experiment_id=client.get_experiment_by_name(model_name).experiment_id
    runs=client.search_runs(experiment_ids=[experiment_id],filter_string=f"tags.version='{version}'")
    
    if runs:
        run_id=runs[0].info.run_id
        model_uri=f"runs:/{run_id}/model"
        return model_uri
    else:
        return None
 
    
    
