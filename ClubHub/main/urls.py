from django.urls import path
from . import views


app_name = "main"


urlpatterns = [
  path("", views.home_page_view, name= "home_page_view"),
  path("mode/<mode>", views.mode_view, name= "mode_view"),
  path("search", views.search_view, name= "search"),
  path("create/contact", views.create_contact, name= "create_contact"),
]