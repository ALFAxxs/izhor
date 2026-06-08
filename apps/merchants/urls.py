from django.urls import path
from . import views

urlpatterns = [
    path('',                                    views.dashboard_home,   name='dashboard'),
    path('templates/',                          views.templates_list,   name='templates-list'),
    path('templates/new/',                      views.template_new,     name='template-new'),
    path('templates/<int:pk>/builder/',         views.template_builder, name='template-builder'),
    path('qrcodes/',                            views.qrcodes_page,     name='qrcodes'),
    path('qrcodes/<int:pk>/',                   views.qrcodes_page,     name='qrcode-detail'),
    path('analytics/',                          views.analytics_page,   name='analytics'),

    # Taklifnomalar (to'y, osh)
    path('events/',                             views.events_list,      name='events-list'),
    path('events/new/',                         views.event_builder,    name='event-new'),
    path('events/<int:pk>/edit/',               views.event_builder,    name='event-edit'),
]
