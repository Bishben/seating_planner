from django.urls import path, include
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.home),
    path('events/', views.events, name='events'),
    path('events/finals2024/',views.eventsinstance, name='eventsinstance'),
    path('subjects/', views.subjects, name='subjects'),
    path('branches/', views.branches, name='branches'),
    path('rooms/', views.rooms, name='rooms'),
    path('history/', views.object_history, name='history')
]