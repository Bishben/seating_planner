from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Subject, Branch

# Create your views here.
def home(request):
    return redirect('events')

def events(request):
    return render(request, "home_page/events.html")

def get_subjects_by_branch(request):
    branch_id = request.GET.get('branch_id')
    subjects = Subject.objects.filter(branches__id=branch_id).values("id", "code")
    return JsonResponse({"subjects": list(subjects)})