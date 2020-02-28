from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    major = models.CharField(max_length=75)
    major2 = models.CharField(max_length=75, blank=True)
    email = models.EmailField(max_length=254)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return (self.first_name + " " + self.last_name) 