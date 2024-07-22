from django.urls import path, include
from .views import ModelVersionViewSet, register_model, predict, compare_model_versions, get_model_metrics
from rest_framework.routers import DefaultRouter
from api.middleware import PrometheusMiddleware

router = DefaultRouter()
router.register(r'model-versions', ModelVersionViewSet)

urlpatterns = [
    path('register_model/', register_model, name='register_model'),
    path('predict/', predict, name='predict'),
    path('compare_model_versions/<str:model_name>/', compare_model_versions, name='compare_model_versions'),
    path('get_model_metrics/<str:model_name>/', get_model_metrics, name='get_model_metrics'),
    path('metrics/', PrometheusMiddleware.metrics_view, name='metrics'),
    path('', include(router.urls)),
    path('', include('django_prometheus.urls')),
]
