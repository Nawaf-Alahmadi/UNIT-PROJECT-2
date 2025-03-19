from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
# Database
from .models import Club, Membership
from events.models import Event
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone


# Create your views here.

# All clubs  page
def clubs_page_view(request: HttpRequest):
  clubs = Club.objects.annotate(approved_member_count=Count('memberships', filter=Q(memberships__status="APPROVED")))
  return render(request, "clubs/all_clubs.html", {'clubs' : clubs})

# Request to join view (Student)
def join_club_view(request, club_id):
    if request.user.is_superuser or request.user.is_staff:
        messages.success(request, "Admin and Leaders Can not join clubs", "error")
        return redirect("main:home_page_view")  
        
    club = Club.objects.get(pk= club_id)
    if not Membership.objects.filter(user=request.user, club=club).exists(): # If user and club not exists that means this is first time user rquest to join          
        Membership.objects.create(user=request.user, club=club)
        messages.success(request, "Membership request sent.", "success")
    else:
        messages.error(request, "You have already requested to join.", "error")
    
    return redirect("main:home_page_view")  

# Club manage view (Leader)
def club_manage_view(request:HttpRequest):
  if not request.user.is_staff or request.user.is_superuser:
    return redirect("main:home_page_view")
  if Club.objects.filter(leader= request.user).exists():
    managed_club = Club.objects.get(leader= request.user)
    pending_members = Membership.objects.filter(club= managed_club, status= "PENDING")
    approved_members = Membership.objects.filter(club= managed_club, status= "APPROVED")
    return render(request, "clubs/club_manage.html", {'pending_members': pending_members, 'approved_members': approved_members})
  else:
    messages.error(request,"You do not lead a club", 'error')
    return redirect("main:home_page_view")

# Approve join Requests (Leader)
def approve_member_view(request:HttpRequest,request_id):

  if not request.user.is_staff:
    return redirect("main:home_page_view")
  member_status = Membership.objects.get(pk= request_id)
  member_status.status = "APPROVED"
  member_status.joined_at= timezone.now()
  member_status.save()
  messages.success(request, f"{member_status.user.username} has been approved.")

  return redirect("clubs:club_manage_view")

# Reject join Requests (Leader)
def reject_member_view(request:HttpRequest, request_id):
  if not request.user.is_staff:
    return redirect("main:home_page_view")
  
  member_status = Membership.objects.get(pk= request_id)
  member_status.status = "REJECTED"
  member_status.save()
  messages.success(request, f"{member_status.user.username} has been rejected.")

  return redirect("clubs:club_manage_view")


# Create Club (Admin)
def create_club_view(request:HttpRequest):
  if request.method == "POST":
    # description
    leader_obj = User.objects.get(id= request.POST['leader'])
    new_club = Club(name= request.POST['name'], description= request.POST['description'], image= request.FILES['image'], leader= leader_obj )
    new_club.save()
    messages.success(request, "Club created successfully", "success")
    # 
  leaders = User.objects.filter(is_staff= True,is_superuser= False).exclude(led_club__isnull=False)
  return render(request, "clubs/create_club.html", {"leaders" : leaders})

# 

def modify_club_view(request:HttpRequest, club_id):
  if not request.user.is_staff or request.user.is_superuser:
    messages.warning(request,"Access Denied - Only Club Leader")
    return redirect("main:home_page_view")
  
  club_details = Club.objects.get(pk= club_id)

  if request.method == "POST":
    club_details.name= request.POST['name']
    club_details.description= request.POST['description']
    if 'image' in request.FILES:
      club_details.image = request.FILES['image']
    club_details.save()
    return redirect("clubs:club_details_view", club_id)
    
  return render(request, "clubs/modify_club.html", {'club_details':club_details})

  # Club Detailes 
def club_details_view(request:HttpRequest, club_id):
  club_details = Club.objects.get(pk= club_id)
  members_of_club = User.objects.filter(memberships__club=club_details, memberships__status="APPROVED") # check it again
  if request.user.is_authenticated:
    if Membership.objects.filter(user= request.user , club= club_details).exists() or club_details.leader == request.user:
      private_events = Event.objects.filter(visibility= "PRIVATE", club=club_details)
      return render(request, "clubs/club_details.html", {'club_details' : club_details, 'members_of_club':members_of_club, "private_events":private_events})
  return render(request, "clubs/club_details.html", {'club_details' : club_details, 'members_of_club':members_of_club})


# 

def leave_member_view(request:HttpRequest, club_id, user_id):
  user = User.objects.get(pk= user_id)
  club = Club.objects.get(pk= club_id)
  membership = Membership.objects.get(user= user, club= club)
  membership.delete()
  return redirect("users:users_profile_view", user_id)