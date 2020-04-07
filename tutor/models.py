from django.db import models
from django.contrib.auth.models import User

class Ask(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sending_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiving_user')
    course = models.CharField(max_length=100)
    question = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
    	return (self.sender.profile.first_name + " " + self.sender.profile.last_name + " - " + self.course)