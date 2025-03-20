from django.db import models
from clubs.models import Club
from django.contrib.auth.models import User

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


class RSVP(models.Model):
    class RSVPChoices(models.TextChoices):
      GLOBAL = 'ATTENDING', 'Attending'   
      PRIVATE = 'INTERESTED', 'Interested'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rsvps")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    status = models.CharField(max_length=10, choices=RSVPChoices.choices)

    class Meta:
        unique_together = ("user", "event")

