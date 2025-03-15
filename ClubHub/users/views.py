from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

# Register a user    
def register_page_view(request: HttpRequest):
  if request.method == "POST":
    try:
      new_user = User.objects.create_user(username= request.POST['username'], password= request.POST['password'], email= request.POST['email'], first_name= request.POST['first_name'], last_name= request.POST['last_name'])
      new_user.save()
      messages.success(request,"Registered successfully", "success")
      return redirect("users:login_page_view")
    except Exception as e: 
      messages.error(request,"Not Registered successfully", "error")
      return render(request, "users/register.html")


  return render(request, "users/register.html")

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
  return render(request, "users/login.html")

# Logout a user
def logout_view(request: HttpRequest):
  logout(request)
  messages.success(request,"Logged out successfully", "logout-success")
  return redirect("main:home_page_view")




