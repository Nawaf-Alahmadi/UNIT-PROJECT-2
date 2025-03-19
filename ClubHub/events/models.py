from django.db import models
from clubs.models import Club

# Create your models here.

class Event(models.Model):
  class VisibilityChoices(models.TextChoices):
    GLOBAL = 'GLOBAL', 'Global'   
    PRIVATE = 'PRIVATE', 'Private'

  title = models.CharField(max_length=128)
  description = models.TextField()
  date = models.DateField()
  image = models.ImageField(upload_to="images/events/", default="images/default.png")
  visibility = models.CharField(max_length=10, choices=VisibilityChoices.choices)
  created_at = models.DateTimeField(auto_now_add= True)
  club = models.ForeignKey(Club, on_delete=models.CASCADE)
