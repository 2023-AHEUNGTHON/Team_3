from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
import json
from myapp.models import Category, Popup
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Popupserializer
from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework.renderers import TemplateHTMLRenderer

#mbti별로 팝업스토어 나눈 거 보이도록
class ResultView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'result.html'
    
    @csrf_exempt
    def get(self, request):
        popups = Popup.objects.all()
        serialized_data = []

        for popup in popups:
            serialized_popup = {
                'mbti': popup.mbti,
                'name': popup.name,
                'location': popup.location,
                'time': popup.time,
                'website': popup.website,
                'popup_image': popup.popup_image.url if popup.popup_image else None,
                'id': popup.id,
                'info':popup.info,
                'etc':popup.etc,
            }
            serialized_data.append(serialized_popup)

        return Response({'popup_stores': serialized_data})

    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
            mbti = data.get('mbti', '')
            print(f"MBTI: {mbti}")
            popup_store = Popup.objects.get(mbti=mbti)
            
            serializer = Popupserializer(popup_store)
            serialized_data = serializer.data

            return JsonResponse({'popup_store': serialized_data})
        except Popup.DoesNotExist:
            return JsonResponse({'error': 'No popup store information available for the selected MBTI.'}, status=404)



class SurveyView(View):
    questions = [
        {'id':1,'text': '친구한테 갑자기 놀자는 전화가 올때의 나는?', 'choices':['E', 'I']},
        {'id':2,'text': '혼자 놀아야하는 상황에서 나는?', 'choices':['E','I']},
        {'id':3,'text': '친구랑 길을 걷고 있는데 친구가 갑자기 춤을 춘다. 이때 나는?', 'choices':['E','I']},
        {'id':4,'text': '자고 일어났더니 정수리에 꽃이 폈다.', 'choices':['N','S']},
        {'id':5,'text': '팝업스토어에 가려고 지하철을 탔는데 내 옆자리에만 사람이 앉지 않는다.', 'choices':['N','S']},
        {'id':6,'text': '어떤 결정을 내렸을 때의 나는?', 'choices':['N','S']},
        {'id':7,'text': '“달 보니까 너 생각나서 연락했어”라고 친구한테 문자가 왔다.', 'choices':['F','T']},
        {'id':8,'text': '시계를 보니 지각할 것 같다. 이때 나는?', 'choices':['F','T']},
        {'id':9,'text': '상사가 내 카톡을 읽씹했다.', 'choices':['F','T']},
        {'id':10,'text': '내일 약속을 위해 계획을 세운 나! 어떤 계획이 내 계획?', 'choices':['J','P']},
        {'id':11,'text': '열심히 준비한 일정에 차질이 생겼다.', 'choices':['J','P']},
        {'id':12,'text': '사전예약 팝업스토어에 가기 위해 나는', 'choices':['J','P']},
    ]

    def get(self, request):
        return render(request, 'survey.html',{'question':self.questions})

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        #user_answers = data.get('answers', [])
        #question_id = data.get('questionId')
        result = data.get('result')
        if result is None:
            print(result)
            return JsonResponse({'message': 'Result not provided.'})

        mbti = result
        recommended_popup_data = self.recommended_popup(mbti)
        print(result)
        return JsonResponse({
            'message':f'결과: {mbti}',
            'recommended_popup': [recommended_popup_data],
            'id': recommended_popup_data['id'] if recommended_popup_data else None
        })

    def recommended_popup(self, result):
        popup = None
        mbti_mapping = {
                'ENFP': 1,
                'ENFJ': 2,
                'ENTP': 3,
                'ENTJ': 4,
                'ESFP': 5,
                'ESFJ': 6,
                'ESTP': 7,
                'ESTJ': 8,
                'INFP': 9,
                'INFJ': 10,
                'INTP': 11,
                'INTJ': 12,
                'ISFJ': 13,
                'ISTP': 14,
                'ISTJ': 15,
                'ISFP': 16,
        }
        #초기화
        json.dumps(str(Popup.popup_image))
        serialized_data = {
            'mbti': None,
            'name': None,
            'location': None,
            'time': None,
            'website': None,
            'popup_image': None,
            'id': None,
            'info': None,
            'etc':None,
        }
        print("mbti_mapping:", mbti_mapping)
        print("Result MBTI:", result)
        popup_id = mbti_mapping.get(result)
        print("Popup ID: ", popup_id)

        if popup_id is not None:
            try:
                popup = Popup.objects.get(id=popup_id)
            except Popup.DoesNotExist:
                print(f"Popup with id {popup_id} does not exist.")
        else:
            print(f"Invalid mbti value: {result}")


        if popup:
            serialized_data = {
                'mbti': popup.mbti,
                'name': popup.name,
                'location': popup.location,
                'time': popup.time,
                'website': popup.website,
                'popup_image': popup.popup_image.url if popup.popup_image else None,
                'id': popup.id,
                'info':popup.info,
                'etc':popup.etc,
            }
        print(serialized_data)
        return serialized_data
        #serializer = popup_serilalizer(popup)
        #return render(self.request, 'result.html', {'popup':serializer.data, 'id':id}) 
        #return JsonResponse({'popup':serialized_data, 'id':popup.id})
        #return render('result.html', {'id':id})

#mbti계산 함수
    def calculate_mbti(self, user_answers):
        elements_counter = {'E': 0, 'I': 0, 'N': 0, 'S': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

        for answer in user_answers:
            question_id = answer.get('name')
            if question_id == 'csrfmiddlewaretoken': #토큰 제외시키기
                continue
            answer_elements = answer.get('value')
            elements_counter[answer_elements] += 1

        mbti = ''
        for element, count in elements_counter.items():
            if count >= 2:
                mbti += element

        #print(f"Calculated MBTI: {mbti}")
        return mbti









def home(request):
    return render(request, 'home.html')  # 'home.html'은 홈페이지 템플릿 파일입니다.
    
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def calculate_distance(user_location, store_location):
    x_diff = user_location[0] - store_location[0]
    y_diff = user_location[1] - store_location[1]
    
    return math.sqrt(x_diff**2 + y_diff**2)

@method_decorator(csrf_exempt, name='dispatch')
class StoreRecommendationView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_location = tuple(data.get('user_location'))
        user_interests = data.get('user_interests')
        distance_limit = data.get('distance_limit')
        
        recommended_stores = []
        for store in stores:
            if store["category"] in user_interests:
                distance = calculate_distance(user_location, store["location"])
                if distance < distance_limit:
                    recommended_stores.append(store)
        
        return JsonResponse({'recommended_stores': recommended_stores})
    
    def get(self, request, *args, **kwargs):
        return render(request, 'recommend_store.html')
