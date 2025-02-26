from django.urls import path, include
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.home),
    path('events/', views.events, name='events'),
    path('events/finals2024/',views.eventsinstance, name='eventsinstance'),
    path('exams/', views.exams, name='exams'),
    path('branches/', views.branches, name='branches'),
    path('rooms/', views.rooms, name='rooms'),
]