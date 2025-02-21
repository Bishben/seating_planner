from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return redirect('events')

def events(request):
    return render(request, "home_page/events.html")