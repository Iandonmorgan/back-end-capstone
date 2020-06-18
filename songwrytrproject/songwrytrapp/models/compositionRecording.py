from django.db import models
from django.urls import reverse
from .composition import Composition
from .recording import Recording

class CompositionRecording(models.Model):

    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)
    ownership_split = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("compositionrecording")
        verbose_name_plural = ("compositionrecordings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("compositionrecording_detail", kwargs={"pk": self.pk})
