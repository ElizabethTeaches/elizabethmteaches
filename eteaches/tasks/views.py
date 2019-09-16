from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Image, UploadSecret
import os

# Create your views here.
def index(request):
    return HttpResponse('This is the tasks index - this is not intended to'
                        + ' be used.')

@csrf_exempt
def upload_file(request):
    if request.method != 'POST':
        return HttpResponseNotFound()

    if 'secret' not in request.POST:
        return JsonResponse(
            {
                'success': False,
                'error': 'missing secret'
            },
            status=400)

    secret = request.POST['secret']
    try:
        upload_secret = UploadSecret.objects.get(secret=secret)
    except ObjectDoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'error': 'not authorized'
            },
            status=400)

    if len(request.FILES) != 1:
        return JsonResponse({
            'success': False,
            'error': f'expected 1 file, got {len(request.FILES)}'},
            status=400)

    file_n = list(request.FILES)[0]
    file_ext = os.path.splitext(file_n)[1]  # trusted input
    _file = request.FILES[file_n]

    img = Image(upload_secret=upload_secret)
    img.save()

    img_file = hex(img.id) + file_ext
    outfile = os.path.join(settings.TASKS_UPLOAD_DIR, img_file)

    os.makedirs(settings.TASKS_UPLOAD_DIR, exist_ok=True)

    with open(outfile, 'wb') as outfile:
        for chunk in _file.chunks():
            outfile.write(chunk)

    return JsonResponse(
        {
            'success': True,
            'filename': img_file
        }, status=200)
