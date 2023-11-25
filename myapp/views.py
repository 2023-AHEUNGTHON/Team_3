import json
from django.shortcuts import render, redirect
from .models import Popup

def home(request):
    return render(request, 'home.html')

def survey(request):
    if request.method == 'GET':
        return render(request, 'survey.html')
    if request.method == 'POST':
        # data = json.loads(request.body)
        # print('aaaaa')
        # print(data)
        # usermbti = data.get('result')
        print('bbbbbbbb')
        # print(usermbti)
        usermbti = 'ESTJ'
        return redirect('result', usermbti)
        # return usermbti

def result(request, usermbti):
    if request.method == 'GET':
        print(usermbti)
        popup = Popup.objects.get(mbti=usermbti)
        print("popup: ")
        print(popup)
        return render(request, 'result.html', {'popup':popup})