from django.test import TestCase,Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import ModelVersion
import joblib
import json
import os
from sklearn.linear_model import LogisticRegression
import joblib
import mlflow.sklearn
import os

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a dummy model for testing
        self.model = LogisticRegression()
        self.model.fit([[0, 0], [1, 1]], [0, 1])
        self.model_path = "test_model.pkl"
        joblib.dump(self.model, self.model_path)

        self.register_url = reverse('register_model')
        self.predict_url = reverse('predict')

    
    def test_register_model(self):
        data = {
            'name': 'test_model',
            'version': 1.0,
            'description': 'Test model description',
            'model_path': self.model_path
        }
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('run_id', response.data)
        self.model_version_id=ModelVersion.objects.first().id

    def test_predict(self):
        predict_data = {
            'input_data': [0, 0],
            'model_name': "test_model",

        }
        response=self.client.post(self.predict_url,predict_data,content_type='application/json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('prediction',response.data)

    def tearDown(self):
        if os.path.exists(self.model_path):
            os.remove(self.model_path)
            
if __name__=="__main__":
    TestCase.main()