from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from clubs.models import Club, Membership
from events.models import Event
from .models import Contact
from django.db.models import Avg, Sum, Count, Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
# from django.template.loader import render_to_string 

# Create your views here.

def home_page_view(request: HttpRequest):
  clubs = Club.objects.annotate(approved_member_count=Count('memberships', filter=Q(memberships__status= "APPROVED"))).order_by('-approved_member_count')[0:3]
  events = Event.objects.annotate(attendance_count= Count('rsvps', filter=Q(rsvps__status= 'ATTENDING'))).filter(visibility="GLOBAL").order_by('-attendance_count')[0:3]
  return render(request, "main/index.html", {'clubs':clubs, 'events':events})

def mode_view(request: HttpRequest, mode):
  next = request.GET.get("next", "/")
  response = redirect(next)

  if mode == "dark":
    response.set_cookie("mode", "dark")
  if mode == "light":
    response.set_cookie("mode", "light")

  return response

def search_view(request:HttpRequest):
  if "search" in request.GET:
    clubs = Club.objects.filter(name__contains= request.GET['search'])
    events = Event.objects.filter(title__contains= request.GET['search'])
    return render(request,"main/search.html", {'clubs':clubs, 'events':events})


def create_contact(request:HttpRequest):
  if 'POST' == request.method:
    new_contact = Contact(name = request.POST['name'], email = request.POST['email'], message = request.POST['message'])
    new_contact.save()
    messages.success(request, "Your message is sent", "success")

    # Send email
    content = "We have received your message. Thank you for reaching out to us. We'll get back to you soon."
    send_to = new_contact.email
    email_message = EmailMessage("Confiramation - Message Received", content, settings.EMAIL_HOST_USER, [send_to])
    # email_message.content_subtype = "html"
    email_message.send()

    return redirect('main:home_page_view')
