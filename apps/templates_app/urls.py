from django.urls import path
from . import views

urlpatterns = [
    path('categories/',                      views.category_list,          name='categories'),
    path('templates/',                       views.template_list,          name='template-list'),
    path('templates/<int:pk>/',              views.template_detail,        name='template-detail'),
    path('templates/<int:pk>/config/',       views.template_config_update, name='template-config'),
    path('audio/',                           views.audio_list,             name='audio-list'),

    # Taklifnomalar (to'y, osh)
    path('events/',                          views.event_template_list,    name='event-list'),
    path('events/<int:pk>/',                 views.event_template_detail,  name='event-detail'),
]
