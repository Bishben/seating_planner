from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Subject, Branch

# Create your views here.
def home(request):
    return redirect('home_page:events')

def events(request):
    return render(request, "home_page/events.html")

def subjects(request):
    return render(request, "home_page/subjects.html")

def branches(request):
    return render(request, "home_page/branches.html")

def rooms(request):
    return render(request, "home_page/rooms.html")

def eventsinstance(request):
    return render(request, "home_page/ExamRoom.html")
