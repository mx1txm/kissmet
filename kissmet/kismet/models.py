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
    Titel = models.CharField(max_length=100)
    Beschreibung = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Adresse = models.CharField(max_length=100)
    Mindestpreis = models.CharField(max_length=100)
    Hoechstpreis = models.CharField(max_length=100)
    maxGaesteanzahl = models.CharField(max_length=100)

    city_choices = (
        ('Berlin', 'Berlin'),
        ('Bielefeld', 'Bielefeld'),
        ('Frankfurt', 'Frankfurt'),
        ('München', 'München'),
        ('Hamburg', 'Hamburg'),
        ('Köln', 'Köln'),
    )

    Stadt = models.CharField(max_length=15, choices=city_choices, default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
