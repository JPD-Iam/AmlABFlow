
from abc import ABC, abstractmethod
class BasePlugin(ABC):
    @abstractmethod
    def log_model(self, experiment_id,model_path, model_name, description, version, accuracy, model_type):
        pass
    def predict(self,data):
        raise NotImplementedError("Subclasses should implement this method")
    
    def load_model(self,model_path):
        raise NotImplementedError("Subclasses should implement this method")
