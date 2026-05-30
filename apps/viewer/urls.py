from django.urls import path
from . import views

urlpatterns = [
    path('<str:slug>/', views.viewer, name='viewer'),
]
