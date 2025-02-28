from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from .models import Subject, Branch, Event, Room

# Create your views here.
def home(request):
    return redirect('home_page:events')

def subjects(request):
    subjects = Subject.objects.all()  # Fetch all subjects
    return render(request, 'home_page/subjects.html', {'subjects': subjects})

def branches(request):
    branches = Branch.objects.all()
    context = {'branches': branches}
    return render(request, "home_page/branches.html", context)

def events(request):
    events = Event.objects.all()  # Fetch all events
    return render(request, 'home_page/events.html', {'events': events})

def rooms(request):
    rooms = Room.objects.all()
    return render(request, "home_page/rooms.html", {"rooms": rooms})

def eventsinstance(request):
    return render(request, "home_page/ExamRoom.html")

def object_history(request, app_label=None, model_name=None, object_id=None):
    if app_label and model_name and object_id:
        from django.contrib.contenttypes.models import ContentType
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())
            history = LogEntry.objects.filter(content_type=content_type, object_id=object_id).order_by('-action_time')
        except ContentType.DoesNotExist:
            history = []
    else:
        history = LogEntry.objects.all().order_by('-action_time')[:10]  # Show recent logs by default

    return render(request, 'home_page/history.html', {'history': history})
