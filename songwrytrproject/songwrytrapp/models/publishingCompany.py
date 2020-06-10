from django.db import models
from django.contrib.auth.models import User
from .pro import PRO

class PublishingCompany(models.Model):

    user = models.ForeignKey(User, verbose_name=("publishingcompanies"), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    admin = models.CharField(max_length=255, null=True, blank=True)
    pro = models.ForeignKey(PRO, on_delete=models.CASCADE)
    pro_acct_num = models.IntegerField()

    class Meta:
        verbose_name = ("publishingcompany")
        verbose_name_plural = ("publishingcompanies")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("publishingcompany_detail", kwargs={"pk": self.pk})
