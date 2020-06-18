from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .composition import Composition

class Recording(models.Model):

    user = models.ForeignKey(User, verbose_name=("recordings"), on_delete=models.CASCADE)
    audio_url = models.CharField(max_length=255)
    producer = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    recording_type = models.CharField(max_length=50)
    date_recorded = models.DateField(auto_now=False, auto_now_add=False)
    is_mixed = models.BooleanField()
    is_mastered = models.BooleanField()
    is_delivered = models.BooleanField()
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)
    ownership_split = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("recording")
        verbose_name_plural = ("recordings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recording_detail", kwargs={"pk": self.pk})
