from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import make_aware
import datetime


# Create your models here.
class Post(models.Model):
	text = models.CharField(max_length=45, null=True)
	person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	time = models.TimeField(auto_now_add=True, null=True)
	date = models.DateField(auto_now_add=True, null=True)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.text

	def get_changes(timestamp=0):
		t = make_aware(datetime.datetime.fromtimestamp(timestamp / 1000.0))
		return Post.objects.filter(last_modified__gt=t).distinct()

	@property
	def html(self):
		return render_to_string("post.html", {"person": self.person, "post": self.text,
						      "time": self.time, "date": self.date,
						      "post_id": self.id}).replace("\n", "")


class Comment(models.Model):
	text = models.CharField(max_length=45, null=True)
	person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
	time = models.TimeField(auto_now_add=True, null=True)
	date = models.DateField(auto_now_add=True, null=True)

	def __str__(self):
		return self.text

	@property
	def html(self):
		return render_to_string("comment.html", {"person": self.person, "comment": self.text,
							 "post_id": self.post.id, "date": self.date,
							 "time": self.time}).replace("\n","")

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.IntegerField(validators=[MaxValueValidator(200), MinValueValidator(0)], null=True)
	bio = models.CharField(max_length=420, null=True, blank=True)
	avatar = models.ImageField(upload_to='avatar', default='avatar/default.png', blank=True)
	followees = models.ManyToManyField(User, related_name="follow_user")

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

