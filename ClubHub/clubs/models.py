from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Club(models.Model):
  name = models.CharField(max_length=128)
  description = models.TextField()
  image = models.ImageField(upload_to="images/", default="images/default.png")
  leader = models.OneToOneField(
      User, 
      on_delete=models.SET_NULL, 
      null=True, 
      blank=True,
      limit_choices_to={'is_staff': True},  # Only leaders can be assigned
      related_name='led_club',
  )
  created_at = models.DateTimeField(auto_now_add=True)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    status = models.CharField(max_length=10,default='PENDING')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'club')  # Prevent duplicate memberships
