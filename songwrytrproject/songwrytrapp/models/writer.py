from django.db import models
from django.contrib.auth.models import User
from .pro import PRO

class Writer(models.Model):

    user = models.ForeignKey(User, verbose_name=("writers"), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    publishing_notes = models.CharField(max_length=255)
    pro = models.ForeignKey(PRO, on_delete=models.CASCADE)
    pro_acct_num = models.IntegerField()

    class Meta:
        verbose_name = ("writer ")
        verbose_name_plural = ("writers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("writer_detail", kwargs={"pk": self.pk})
