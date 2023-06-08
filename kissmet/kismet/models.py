from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Author(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    adress = models.CharField(max_length=100)
    min_price = models.CharField(max_length=100)
    max_price = models.CharField(max_length=100)
    max_guest = models.CharField(max_length=100)

    city_choices = (
        ('Berlin', 'Berlin'),
        ('Bielefeld', 'Bielefeld'),
        ('Frankfurt', 'Frankfurt'),
        ('München', 'München'),
        ('Hamburg', 'Hamburg'),
        ('Köln', 'Köln'),
    )

    city = models.CharField(max_length=15, choices=city_choices, default=0)

    #location_style_choices = (
       # ('Schloss', 'Schloss'),
       # ('Scheune', 'Scheune'),
    #)
    #location_type = models.CharField(max_length=15, choices=location_style_choices, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


#FOR WEBSCRAPING

class ScrapedData(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title