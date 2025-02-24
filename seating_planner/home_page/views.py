from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return redirect('events')

def events(request):
    return render(request, "home_page/events.html")

def exams(request):
    return render(request, "home_page/exams.html")

def branches(request):
    return render(request, "home_page/branches.html")

def rooms(request):
    return render(request, "home_page/rooms.html")

def eventsinstance(request):
    return render(request, "home_page/ExamRoom.html")