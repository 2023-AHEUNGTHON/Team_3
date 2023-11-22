from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
import json
from myapp.models import Category, popup
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from .serilalizers import popup_serilalizer

#mbti별로 팝업스토어 나누기
class ResultView(APIView):
    def get(self, request):
        return render(request, 'result.html', {'popup':None})
    def post(self, request):
        data = request.data
        result = "".join(data['result'])

        #render로 사용자에게 정보 보여주기
        try:
            popup_store = popup.objects.get(mbti=result)
            serializer = popup_serializer(popup_store)
            return render(request, 'result.html', {'popup': serializer.data})
        except popup.DoesNotExist:
            return render(request, 'result.html', {'popup': None})

        if result == 'ENFP':
            popup = popup.objects.get(id=1)
        elif result == 'ENFJ':
            popup = popup.objects.get(id=2)
        elif result == 'ENTP':
            popup = popup.objects.get(id=3)
        elif result == 'ENTJ':
            popup = popup.objects.get(id=4)
        elif result == 'ESFP':
            popup = popup.objects.get(id=5)  
        elif result == 'ESFJ':
            popup = popup.objects.get(id=6)
        elif result == 'ESTP':
            popup = popup.objects.get(id=7)
        elif result == 'ESTJ':
            popup = popup.objects.get(id=8)
        elif result == 'INFP':
            popup = popup.objects.get(id=9)
        elif result == 'INFJ':
            popup = popup.objects.get(id=10)
        elif result == 'INTP':
            popup = popup.objects.get(id=11)
        elif result == 'INTJ':
            popup = popup.objects.get(id=12)
        elif result == 'ISFJ':
            popup = popup.objects.get(id=13)
        elif result == 'ISTP':
            popup = popup.objects.get(id=14)
        elif result == 'ISTJ':
            popup = popup.objects.get(id=15)
        elif result == 'ISFP':
            popup = popup.objects.get(id=16)

        '''
        serializer = popup_serilalizer(popup)
        return Response(serializer.data) '''

def home(request):
    return render(request, 'home.html')  # 'home.html'은 홈페이지 템플릿 파일입니다.
    
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


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

    def recommended_popup(self, mbti):
        if mbti and mbti[0] == 'E': #테스트용
            return '푸바오'
        else:
            return '향수'

        '''store_mapping = {
            'ENFP': ['푸바오 팝업 스토어'],
            #대충 나머지 추가.....하기...
        }'''
        #return store_mapping.get(mbti_result, [])

    def get(self, request):
        return render(request, 'survey.html',{'question':self.questions})

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        user_answers = data.get('answers', [])
        question_id = data.get('questionId')

        mbti = self.calculate_mbti(user_answers)
        recommended_popup = self.recommended_popup(mbti)

        return JsonResponse({
            'message':f'결과: {mbti}',
            'recommended_popup': recommended_popup
        })

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
