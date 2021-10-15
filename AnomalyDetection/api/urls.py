from django.urls import path
from .views import Prediction

urlpatterns = [
    # Define the endpoint for predictions
    path('predict/', Prediction.as_view(), name = 'prediction'),
]