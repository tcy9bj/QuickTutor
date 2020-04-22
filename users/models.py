from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image
from tutor.models import Ask

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics', blank=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	major = models.CharField(max_length=75)
	major2 = models.CharField(max_length=75, blank=True)
	phone_regex = RegexValidator(regex=r'([0-9]{3}-){2}[0-9]{4}', message="Phone number must be entered in the format: 999-999-9999.")
	phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=False)
	courses = models.TextField(blank=True, help_text="List any courses you feel comfortable tutoring for.")
	description = models.TextField(blank=True)
	location = models.CharField(max_length=50, blank=True, default='')
	current_client = models.OneToOneField(Ask, on_delete=models.SET_NULL, null=True, blank=True)
	tutor_score = models.FloatField(null=True, blank=True)
	num_ratings = models.IntegerField(blank=True, default=0)
	active = models.BooleanField(default=False)
	initialized = models.BooleanField(default=False)

	def __str__(self):
		return (self.first_name + " " + self.last_name + "'s Profile")

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)

		if (img.height > 300 or img.width > 300):
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

	def get_absolute_url(self):
		return reverse('profile_page', kwargs={'pk': self.pk})

class Comment(models.Model):
	reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
	reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewee')
	rating = models.IntegerField()
	comment_text = models.TextField(verbose_name="comment")

	def __str__(self):
		return self.reviewer.profile.first_name + " " + self.reviewer.profile.last_name + "'s review of " + self.reviewee.profile.first_name + " " + self.reviewee.profile.last_name