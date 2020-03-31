from django.db import models
from django.contrib.auth.models import User

class Ask(models.Model):
    fName = models.CharField(max_length=100)
    lName = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    question = models.TextField()

    def __str__(self):
    	return (self.subject)