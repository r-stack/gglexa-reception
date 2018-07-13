
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dialogflow_hook, name='dialogflow_hook'),
]