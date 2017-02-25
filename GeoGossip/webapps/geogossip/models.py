from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save


class Group(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    radius = models.FloatField()
    lifetime = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                              default=1, null=True)
    bio = models.TextField(max_length=420, default="hey there", blank=True)
    picture = models.ImageField(upload_to="add-user-photo", blank=True)
    follower = models.ManyToManyField(User, related_name="follow")

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_profiles(user):
        return Profile.objects.filter(user=user)


class Business(models.Model):
    name = models.CharField(max_length=100)
    categories = models.CharField(max_length=200, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    is_closed = models.BooleanField()
    image_url = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200, null=True)
    display_phone = models.CharField(max_length=200, null=True)
    review_count = models.IntegerField(null=True)
    rating = models.FloatField(null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()
    pass


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

    def __str__(self):
        return self.__unicode__()
    pass


# reference to: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user")
    to_user = models.ManyToManyField(User, related_name="to_user")

    def __unicode__(self):
        return self.from_user.username
    pass
