from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
# Database
from .models import Club, Membership

# Create your views here.

# All clubs  page
def clubs_page_view(request: HttpRequest):
  clubs = Club.objects.all()
  return render(request, "clubs/all_clubs.html", {'clubs' : clubs})


# Request to join view
def join_club_view(request, club_id):
    if request.user.is_superuser:
        messages.success(request, "Admin Can not join clubs", "error")
        return redirect("main:home_page_view")  
        
    club = Club.objects.get(pk= club_id)
    if not Membership.objects.filter(user=request.user, club=club).exists(): # If user and club not exists that means this is first time user rquest to join          
        Membership.objects.create(user=request.user, club=club)
        messages.success(request, "Membership request sent.", "success")
    else:
        messages.error(request, "You have already requested to join.", "error")
    
    return redirect("main:home_page_view")  

# Club manage view
def club_manage_view(request:HttpRequest):
  if not request.user.is_staff:
    return redirect("main:home_page_view")

  managed_club = Club.objects.get(leader= request.user)
  pending_members = Membership.objects.filter(club= managed_club, status= "PENDING")
  approved_members = Membership.objects.filter(club= managed_club, status= "APPROVED")
  
  return render(request, "clubs/club_manage.html", {'pending_members': pending_members, 'approved_members': approved_members})

# Approve join Requests
def approve_member_view(request:HttpRequest,request_id):

  if not request.user.is_staff:
    return redirect("main:home_page_view")
  member_status = Membership.objects.get(pk= request_id)
  member_status.status = "APPROVED"
  member_status.save()
  messages.success(request, f"{member_status.user.username} has been approved.")

  return redirect("clubs:club_manage_view")

# Reject join Requests
def reject_member_view(request:HttpRequest, request_id):
  if not request.user.is_staff:
    return redirect("main:home_page_view")
  
  member_status = Membership.objects.get(pk= request_id)
  member_status.status = "REJECTED"
  member_status.save()
  messages.success(request, f"{member_status.user.username} has been rejected.")

  return redirect("clubs:club_manage_view")
