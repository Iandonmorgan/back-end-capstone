from django.db import models

class PRO(models.Model):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    website = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("pro")
        verbose_name_plural = ("pros")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pro_detail", kwargs={"pk": self.pk})
