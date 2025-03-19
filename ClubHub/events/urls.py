from django.urls import path
from . import views


app_name = "events"


urlpatterns = [
  path("event/create", views.create_event_view, name= "create_event_view"),
  path("events/", views.events_page_view, name= "events_page_view"),
]