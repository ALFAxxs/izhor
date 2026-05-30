from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from apps.merchants.views import login_page, logout_page

urlpatterns = [
    path('',              lambda r: redirect('/auth/login/')),
    path('admin/',        admin.site.urls),
    path('auth/login/',   login_page,   name='login'),
    path('auth/logout/',  logout_page,  name='logout'),
    path('dashboard/',    include('apps.merchants.urls')),
    path('api/auth/',     include('apps.accounts.urls')),
    path('api/',          include('apps.templates_app.urls')),
    path('api/qr/',       include('apps.qr_system.urls')),
    path('i/',            include('apps.viewer.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
