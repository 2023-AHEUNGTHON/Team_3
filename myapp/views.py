from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Category

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def survey_form(request):
    return render(request, 'survey.html')

interest_mapping = {
    "1": "패션",
    "2": "운동",
    "3": "가구"
}

@csrf_exempt
def survey(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        interest_numbers = data.get('interest', [])

        interests = [interest_mapping.get(n, '알 수 없는 관심사항') for n in interest_numbers]
        return JsonResponse({'message': f'설문조사 결과를 성공적으로 받았습니다. 관심사항: {interests}'})
    