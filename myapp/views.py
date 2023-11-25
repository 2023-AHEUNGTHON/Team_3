import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Popup

def home(request):
    return render(request, 'home.html')

def survey(request):
    if request.method == 'GET':
        return render(request, 'survey.html')
    if request.method == 'POST':
        data = json.loads(request.body)
        usermbti = data.get('mbti')
        return redirect('result', usermbti)

def result(request, usermbti):
    if request.method == 'GET':
        popup = Popup.objects.filter(mbti=usermbti).get()
        popup = {
                'mbti': popup.mbti,
                'name': popup.name,
                'location': popup.location,
                'time': popup.time,
                'website': popup.website,
                'popup_image': popup.popup_image.url if popup.popup_image else None,
                'id': popup.id,
                'info': popup.info,
                'etc': popup.etc,
        }
        return JsonResponse(popup, safe=False, json_dumps_params={'ensure_ascii': False})
    if request.method == 'POST':
        return redirect(request, 'result.html', {'popup':popup})