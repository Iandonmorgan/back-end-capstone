from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Composition(models.Model):

    user = models.ForeignKey(User, verbose_name=("compositions"), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    alt_titles = models.CharField(max_length=255)
    lyrics = models.TextField()
    notes = models.CharField(max_length=255)
    date_created = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = ("composition")
        verbose_name_plural = ("compositions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("composition_detail", kwargs={"pk": self.pk})
