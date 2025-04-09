from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from clubs.models import Membership, Club
from events.models import Event, RSVP
from django.db.models import Count, Q
from django.core.mail import EmailMessage
from django.conf import settings



# Create your views here.

# Register a user    
def register_page_view(request: HttpRequest):
  if request.method == "POST":
    try:
      new_user = User.objects.create_user(username= request.POST['username'], password= request.POST['password'], email= request.POST['email'], first_name= request.POST['first_name'], last_name= request.POST['last_name'])
      new_user.save()
      messages.success(request,"Registered successfully", "success")

      # Send Email
      content = "Thank you for registering at ClubHub. We’re excited to have you with us!"
      send_to = new_user.email
      email_message = EmailMessage("Welcome to ClubHub!", content, settings.EMAIL_HOST_USER, [send_to])
      # email_message.content_subtype = "html"
      email_message.send()



      return redirect("users:login_page_view")
    except Exception as e: 
      messages.error(request,"Not Registered successfully", "error")
      return render(request, "users/register.html")

  if not request.user.is_authenticated:
    return render(request, "users/register.html")
  else:
    messages.error(request, "You are already registerd")
    return redirect("main:home_page_view")

# Login a user
def login_page_view(request: HttpRequest):
  if request.method == "POST":
    user = authenticate(request, username= request.POST['username'], password= request.POST['password'])
    
    if user:
      login(request, user)
      messages.success(request,"Logged in successfully", "success")
      return redirect("main:home_page_view")
    else:
      messages.error(request,"Not Logged in successfully", "error")
      return render(request, "users/login.html")
  if not request.user.is_authenticated:
    return render(request, "users/login.html")
  else:
    messages.error(request, "You are already logged in")
    return redirect("main:home_page_view")

# Logout a user
def logout_view(request: HttpRequest):
  logout(request)
  messages.success(request,"Logged out successfully", "logout-success")
  return redirect("main:home_page_view")

# Manage user access (Admin)
def manage_users_view(request: HttpRequest):
  if not request.user.is_superuser:
    return redirect("main:home_page_view")
  if request.method == "POST":
    user_ids = request.POST.getlist("user_ids")
    User.objects.filter(id__in= user_ids).update(is_staff= True)
    # Any users not in user_ids = False
    User.objects.exclude(id__in= user_ids).update(is_staff= False)
    Club.objects.filter(leader__in=User.objects.exclude(id__in=user_ids)).update(leader=None)

    messages.success(request, "Updated successfully", "success")
  users = User.objects.all().exclude(is_superuser= True)
  return render(request, "users/manage_users.html", {"users" : users})

# Profile 

def users_profile_view(request: HttpRequest, user_id):
    if not request.user.is_authenticated or request.user.is_superuser:
        return redirect("main:home_page_view")

    user = User.objects.get(pk=user_id)

    user_events = Event.objects.filter(rsvps__user=user).annotate(attendance_count=Count("rsvps", filter=Q(rsvps__status="ATTENDING")))


    if request.user.is_staff:
        leader = User.objects.get(id=user_id)

        if Club.objects.filter(leader=leader).exists():
            leader_managed_club = Club.objects.get(leader=leader)
            events = Event.objects.filter(club=leader_managed_club).annotate(
          attendance_count=Count('rsvps', filter=Q(rsvps__status='ATTENDING'))  
      )

            leader_events = Event.objects.filter(club=leader_managed_club).annotate(attendance_count=Count("rsvps", filter=Q(rsvps__status="ATTENDING")))

            return render(
                request,
                "users/profile.html",
                {
                    "user": user,
                    "events":events,
                    "leader_managed_club": leader_managed_club,
                    "leader_events": leader_events,
                    "user_events": user_events,
                },
            )
        else:
            return render(request, "users/profile.html", {"user": user, "user_events": user_events})

    else:
        user_clubs = Membership.objects.filter(user=user, status="APPROVED")

        return render(
            request,
            "users/profile.html",
            {"user": user, "user_clubs": user_clubs, "user_events": user_events},
        )