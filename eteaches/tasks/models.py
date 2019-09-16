from django.db import models

class UploadSecret(models.Model):
    secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} - {self.secret}'

class Image(models.Model):
    upload_secret = models.ForeignKey(
        UploadSecret, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return hex(self.id)
