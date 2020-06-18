from django.db import models
from django.urls import reverse
from .publishingCompany import PublishingCompany
from .composition import Composition

class CompositionPublishing(models.Model):

    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    publishing_company = models.ForeignKey(PublishingCompany, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    pro_work_num = models.IntegerField()

    class Meta:
        verbose_name = ("compositionpublishing")
        verbose_name_plural = ("compositionpublishings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("compositionpublishing_detail", kwargs={"pk": self.pk})
