from django.urls import path
from . import views


app_name = "clubs"


urlpatterns = [
  path("clubs/", views.clubs_page_view, name= "clubs_page_view"),
  path("clubs/join/<club_id>/", views.join_club_view, name= "join_club_view"),
  path("club/manage/", views.club_manage_view, name= "club_manage_view"),
  path("club/manage/approve/<request_id>", views.approve_member_view, name= "approve_member_view"),
  path("club/manage/reject/<request_id>", views.reject_member_view, name= "reject_member_view"),
]