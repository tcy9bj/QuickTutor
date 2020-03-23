#Some code from: https://medium.com/@jainsahil1997/simple-google-authentication-in-django-58101a34736b
#Some code from: https://www.youtube.com/watch?v=FdVuKt_iuSI&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=8

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.shortcuts import redirect

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		#return redirect('register')


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()