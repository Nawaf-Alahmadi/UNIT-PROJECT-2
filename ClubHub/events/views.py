from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from events.models import Event
from clubs.models import Club
from django.contrib import messages

# Create your views here.

def create_event_view(request:HttpRequest):
  if not request.user.is_staff:
    messages.error(request, "Only Admin and Leaders allowed", "error")
    return redirect("main:home_page_view")
  if Club.objects.filter(leader= request.user).exists():
    club = Club.objects.get(leader= request.user)
  else:
    messages.error(request,"You do not lead a club", "error")
    return redirect("main:home_page_view")
  if request.method == "POST":
    new_event = Event(club= club, title= request.POST['title'], description= request.POST['description'], date= request.POST['date'], visibility= request.POST['visibility'], image= request.FILES['image'])
    new_event.save()
    messages.success(request, "Event created succussfuly")
  return render(request, "events/create_event.html", {"visibility_choices" : Event.VisibilityChoices.choices})

def events_page_view(request:HttpRequest):
  events = Event.objects.filter(visibility= "GLOBAL")
  return render(request, "events/all_events.html", {'events' : events})

