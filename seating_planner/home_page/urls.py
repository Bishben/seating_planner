from django.urls import path, include
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.home),
    path('events/', views.events, name='events'),
    path('events/exams/<int:event_id>/', views.exams, name='exams'),
    path('events/examroom/<int:event_id>/', views.examroom, name='examroom'),
    path('subjects/', views.subjects, name='subjects'),
    path('branches/', views.branches, name='branches'),
    path('rooms/', views.rooms, name='rooms'),
    path('history/', views.object_history, name='history')
]