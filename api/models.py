from django.db import models


class ModelVersion(models.Model):
    model_name= models.CharField(max_length=100)
    version=models.CharField(max_length=20)
    description=models.TextField()
    mlflow_run_id=models.CharField(max_length=100,unique=True)
    accuracy=models.FloatField(default=0.0)
    model_type = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.model_name}-{self.version}"
    
class PredictionLog(models.Model):
        model_name=models.CharField(max_length=100)
        version=models.CharField(max_length=100)
        input_data=models.JSONField()
        prediction= models.JSONField()
        response_time=models.FloatField()
        model_type=models.CharField(max_length=150)
        timestamp=models.DateTimeField(auto_now_add=True)
        def __str__(self):
           return f"{self.model_name}-{self.version}"

     