from django.urls import path
from . import views


app_name = "events"


urlpatterns = [
  path("event/create", views.create_event_view, name= "create_event_view"),
  path("events/", views.events_page_view, name= "events_page_view"),
  path("event/modify/<event_id>/<leader_id>", views.event_modify_view, name= "event_modify_view"),
  path("event/delete/<event_id>/<leader_id>", views.event_delete_view, name= "event_delete_view"),
  path("event/attending/<event_id>/<user_id>/<status>", views.event_attend_interested_view, name= "event_attend_interested_view"),
  path("event/manage/", views.event_manage_view, name= "event_manage_view"),
]