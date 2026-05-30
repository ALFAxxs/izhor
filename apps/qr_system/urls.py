from django.urls import path
from . import views

urlpatterns = [
    path('template/<int:pk>/',     views.qr_detail,        name='qr-detail'),
    path('download/<str:slug>/',   views.qr_download,      name='qr-download'),
    path('analytics/',             views.merchant_analytics, name='analytics'),
]
