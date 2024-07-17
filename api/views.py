from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({"messgae": "Hello, World"})


@api_view(['POST'])
def predict(request):

    #Prediction logic

    data= request.data
    return Response({"prediction": "This is a placeholder prediction"})