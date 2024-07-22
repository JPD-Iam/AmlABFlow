from rest_framework import viewsets,status
from .models import ModelVersion,PredictionLog
from .serializers import ModelVersionSerializer
import mlflow
import mlflow.sklearn
from .mlflow_utils import log_model,create_experiment_if_not_exists,get_model_uri
import json
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
import logging 
import joblib
import random
import numpy as np
import time
from django.db.models import Avg
from rest_framework_api_key.permissions import HasAPIKey
from plugins.plugin_manager import PluginManager
from plugins.sklearn_plugin import SklearnPlugin

plugin = SklearnPlugin()

#use plugin manager to load different plugins in future

logger=logging.getLogger(__name__)
class ModelVersionViewSet(viewsets.ModelViewSet):
    queryset=ModelVersion.objects.all()
    serializer_class=ModelVersionSerializer


def choose_model_version(model_name):
    model_versions=ModelVersion.objects.filter(model_name=model_name)
    if not model_versions.exists():
        return None
    
    model_version_list=list(model_versions)
    accuracies = np.array([version.accuracy for version in model_version_list])

    total_accuracy=accuracies.sum()
    if total_accuracy == 0:
        chosen_version=random.choice(model_versions)
        return chosen_version.version
    
    weights=[version.accuracy for version in model_version_list]
    weights=weights/total_accuracy
    chosen_version=np.random.choice(model_version_list,p=weights)
    return chosen_version.version



@api_view(['GET'])
def get_model_metrics(request,model_name):
    try:
      logs=PredictionLog.objects.filter(model_name=model_name)
      if not logs.exists():
        return Response({'error':'No logs founds for the specified model'},status=status.HTTP_404_NOT_FOUND)
      avg_response_time=logs.aggregate(Avg('response_time'))['response_time__avg']
      metrics={
        'average_response_time':avg_response_time,
        'total_predictions':logs.count()
             }
      return Response(metrics,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def compare_model_versions(request,model_name):
    logs = PredictionLog.objects.filter(model_name=model_name)
    if not logs.exists():
        return Response({'error': 'No logs found for the specified model'}, status=status.HTTP_404_NOT_FOUND)
    versions=logs.values('version').distinct()
    comparison_data={}
    for version in versions:
        version_logs =logs.filter(version=version['version'])
        avg_response_time=version_logs.aggregate(Avg('response_time'))['response_time__avg']
        comparison_data[version['version']]={
        'average_response_time':avg_response_time,
        'total_predictions':version_logs.count()
                 }
    return Response(comparison_data,status=status.HTTP_200_OK)

   
@csrf_exempt
@api_view(['POST'])
def register_model(request ):
    available_model_types = ['sklearn']

    model_name= request.data.get('model_name')
    version=request.data.get('version')
    description=request.data.get('description')
    model_path=request.data.get('model_path')
    accuracy=request.data.get('accuracy')
    model_type=request.data.get('model_type')
    
    if not all([model_name,version,description,model_path,accuracy,model_type]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    if model_type not in available_model_types:
        return Response({'error':f'Invalid model type.Available options are:{",".join(available_model_types)}'},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        run_id=log_model(model_path,model_name,description,version,accuracy,model_type)

        model_version= ModelVersion(
            model_name=model_name,
            version=version,
            description=description,
            accuracy=accuracy,
            model_type=model_type,
            mlflow_run_id=run_id
        )
        model_version.save()
      
        return Response({'run_id':run_id},status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error("Error registering model: %s", str(e))
       
        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def predict(request):
    try: 
        input_data=request.data.get('input_data')
        model_name = request.data.get('model_name')
        model_type=request.data.get('model_type')
        if not plugin:
           return Response({'error':'Model type not supported'},status=status.HTTP_400_BAD_REQUEST)

        if input_data is None or model_name is None :
            return Response({'error': 'Input data and model name are required'},status=status.HTTP_400_BAD_REQUEST)
        version=choose_model_version(model_name)

        model_uri=get_model_uri(model_name,version,model_type)
        
        if model_uri is None:
            return Response({'error':'Model version not found'},status=status.HTTP_404_NOT_FOUND)
        model=plugin.load_model(model_uri)
        start_time=time.time()
        prediction =plugin.predict([input_data])
        response_time=time.time()-start_time

        PredictionLog.objects.create(
            model_name=model_name,
            version=version,
            input_data=input_data,
            prediction=prediction.tolist(),
            response_time=response_time,
            model_type=model_type
        )
        
        logger.info(f'Prediction made using model {model_name} version {version} is : {prediction}')
        return Response({'prediction':prediction.tolist(),
                         'model_version':version,
                         'response_time':response_time,
                         'model_type':model_type
                         })
        
    except ModelVersion.DoesNotExist :
        return Response({'error': 'Model version not found'},status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e :
        logger.error("Error predicting model: %s", str(e))

        return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    