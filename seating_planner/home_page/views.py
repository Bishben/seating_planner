from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Subject, Branch

# Create your views here.
def home(request):
    return redirect('home_page:events')

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

def get_subjects_by_branch(request):
    branch_id = request.GET.get('branch_id')
    subjects = Subject.objects.filter(branches__id=branch_id).values("id", "code")
    return JsonResponse({"subjects": list(subjects)})
