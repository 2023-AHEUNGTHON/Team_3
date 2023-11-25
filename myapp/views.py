import json
from django.shortcuts import render, redirect
from .models import Popup

def home(request):
    return render(request, 'home.html')

def survey(request):
    if request.method == 'GET':
        return render(request, 'survey.html')
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        usermbti = data.get('userMbti')
        print(usermbti)
        return redirect('result', usermbti)

def result(request, usermbti):
    if request.method == 'GET':
        popup = Popup.objects.get(mbti=usermbti)
        print(popup)
        return render(request, 'myapp/result.html', {'popup':popup})