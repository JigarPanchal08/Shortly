from django.db import models

# Create your models here.

class LinksData(models.Model):
    username = models.CharField(max_length=100)
    redirect_link = models.URLField()
    short_id = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.username} : {self.redirect_link}"