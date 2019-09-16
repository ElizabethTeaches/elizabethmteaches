from django.contrib import admin

from .models import UploadSecret, Image

# Register your models here.
admin.site.register(UploadSecret)
admin.site.register(Image)
