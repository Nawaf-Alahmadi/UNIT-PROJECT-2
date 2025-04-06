from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from events.models import Event, RSVP
from clubs.models import Club
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q

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
  events = Event.objects.filter(
    visibility="GLOBAL"
  ).annotate(
      attendance_count=Count('rsvps', filter=Q(rsvps__status='ATTENDING'))  
  )
  
  
  return render(request, "events/all_events.html", {'events' : events})

def event_modify_view(request:HttpRequest, event_id, leader_id):
  event = Event.objects.get(pk= event_id)
  if request.method == "POST":
    event.title= request.POST['title']
    event.description= request.POST['description']
    if 'image' in request.FILES:
      event.image= request.FILES['image']
    event.date= request.POST['date']
    event.visibility= request.POST['visibility']
    event.save()
    return redirect("users:users_profile_view", leader_id)
  return render(request, "events/modify_event.html", {'event':event, 'visibility_choices':Event.VisibilityChoices.choices, "leader_id":leader_id})


def event_delete_view(request:HttpRequest, event_id, leader_id):
  event = Event.objects.get(pk=event_id)
  if request.method == "POST":
    event.delete()
    messages.success(request, "Event deleted successfuly", "success")
    return redirect("users:users_profile_view", leader_id)
  return render(request, "events/delete_event_confirmation.html", {"event" : event, "leader_id":leader_id})


def event_attend_interested_view(request: HttpRequest, event_id, user_id, status):
  if not request.user.is_authenticated:
    messages.warning(request, "You need to login first", 'warning')
    return redirect("events:events_page_view")
  elif request.user.is_superuser:
    messages.warning(request, "Admin are not allowed to attend", 'warning')
    return redirect("events:events_page_view")

  event = Event.objects.get(pk= event_id)
  user = User.objects.get(pk= user_id)

  existing_rsvp = RSVP.objects.filter(user=user, event=event).first()

  if existing_rsvp:
      existing_rsvp.status = status
      existing_rsvp.save()
      messages.success(request, f"RSVP status updated to '{status}'.")
  else:
      new_rsvp = RSVP(user=user, event=event, status=status)
      new_rsvp.save()
      messages.success(request, f"RSVP as '{status}' saved successfully!")

  return redirect("events:events_page_view")  

def event_manage_view(request:HttpRequest):
  if not request.user.is_staff or request.user.is_superuser:
    return redirect("main:home_page_view")
  
  if Club.objects.filter(leader= request.user).exists():
    managed_club = Club.objects.get(leader= request.user)
    events = Event.objects.filter(club=managed_club).annotate(attendance_count=Count('rsvps', filter=Q(rsvps__status='ATTENDING')), intersted_count=Count('rsvps', filter=Q(rsvps__status='INTERESTED'))  )
  return render(request, "events/event_manage.html", {'events':events})