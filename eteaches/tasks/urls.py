from django.urls import path

import tasks.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_file', views.upload_file, name='upload_file')
]
