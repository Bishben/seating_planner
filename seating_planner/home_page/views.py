from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from .models import Subject, Branch, Event, Room, ExamRoom, Exam

# Create your views here.
def home(request):
    return redirect('home_page:events')

def subjects(request):
    subjects = Subject.objects.all()
    query = request.GET.get('q', '')
    if query:
        subjects = subjects.filter(
            Q(code__icontains=query) | Q(branches__name__icontains=query)
        ).distinct()
    return render(request, 'home_page/subjects.html', {'subjects': subjects, 'query':query})

def branches(request):
    branches = Branch.objects.all()
    query = request.GET.get('q', '')
    if query:
        branches = branches.filter(
            Q(name__icontains=query) | Q(year__icontains=query)
        ).distinct()
    return render(request, "home_page/branches.html", {'branches': branches,'query':query})

def events(request):
    events = Event.objects.all() 
    query = request.GET.get('q', '')
    if query:
        events = events.filter(name__icontains=query)
    return render(request, 'home_page/events.html', {'events': events, 'query': query})

def rooms(request):
    rooms = Room.objects.all()
    query = request.GET.get('q', '')
    if query:
        rooms = rooms.filter(type__icontains=query)
    return render(request, "home_page/rooms.html", {"rooms": rooms,'query':query})

def examroom(request, event_id):
    examrooms = ExamRoom.objects.filter(event=event_id) 
    context={'examrooms': examrooms}
    return render(request, 'home_page/ExamRoom.html', context)

def exams(request, event_id):
    exams = Exam.objects.filter(event=event_id) 
    context={'exams': exams}
    return render(request, 'home_page/Exams.html', context)

def object_history(request, app_label=None, model_name=None, object_id=None):
    query = request.GET.get('q', '')
    if app_label and model_name and object_id:
        from django.contrib.contenttypes.models import ContentType
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())
            history = LogEntry.objects.filter(content_type=content_type, object_id=object_id).order_by('-action_time')
        except ContentType.DoesNotExist:
            history = []
    else:
        history = LogEntry.objects.all().order_by('-action_time')
    if query:
        history = history.filter(object_repr__icontains=query)
    history=history[:10]

    return render(request, 'home_page/history.html', {'history': history, 'query': query})
