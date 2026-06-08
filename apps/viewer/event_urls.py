from django.urls import path
from . import views

urlpatterns = [
    path('<str:slug>/', views.event_viewer, name='event-viewer'),
]
