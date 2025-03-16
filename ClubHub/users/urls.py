from django.urls import path
from . import views


app_name = "users"


urlpatterns = [
  path("register/", views.register_page_view, name= "register_page_view"),
  path("login/", views.login_page_view, name= "login_page_view"),
  path("logout/", views.logout_view, name= "logout_view"),
  path("manage/users/", views.manage_users_view, name="manage_users_view"),

]