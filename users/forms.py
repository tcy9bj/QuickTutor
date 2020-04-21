#Some code from: https://medium.com/@jainsahil1997/simple-google-authentication-in-django-58101a34736b
from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
	major2 = forms.CharField(label="2nd Major", required=False)
	phone_number = forms.RegexField(regex=r'([0-9]{3}-){2}[0-9]{4}',
									help_text="Phone number must be entered in the format: 123-456-7890")

	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'major', 'major2', 'phone_number', 'courses', 'description', 'image']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']
