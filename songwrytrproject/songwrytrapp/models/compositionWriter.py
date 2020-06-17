from django.db import models
from django.urls import reverse
from .composition import Composition
from .writer import Writer

class CompositionWriter(models.Model):

    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = ("compositionwriter")
        verbose_name_plural = ("compositionwriters")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("compositionwriter_detail", kwargs={"pk": self.pk})
