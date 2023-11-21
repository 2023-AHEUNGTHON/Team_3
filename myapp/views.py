from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from myapp.models import Category
import math

def home(request):
    return render(request, 'home.html')  # 'home.html'은 홈페이지 템플릿 파일입니다.
    
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

interest_mapping = {
    "1": "패션",
    "2": "운동",
    "3": "가구"
}

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
        data = json.loads(request, body)
        user_answers = data.get('answers',{})

        mbti = self.calculate_mbti(user_answers)
        recommended_popup = self.recommend_popup(mbti)

        return JsonResponse({
            'message':f'결과: {mbt}',
            'recommended_popup': recommended_popup
        })

    def calculate_mbti(self, user_answers):
        elements_counter = {'E': 0, 'I': 0, 'N': 0, 'S': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

        for question_id, answer_elements in user_answers.items():
            elements_counter[answer_elements] += 1

        mbti = ''
        for element, count in elements_counter.items():
            if count >=2:
                mbti += element

        return mbti



    def get_recommended_stores(self, mbti_result):
        store_mapping = {
            'ENFP': ['푸바오 팝업 스토어'],
            #대충 나머지 추가.....하기...
        }

        return store_mapping.get(mbti_result, [])
'''
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        interest_numbers = data.get('interest', [])
        interests = [interest_mapping.get(n, '알 수 없는 관심사항') for n in interest_numbers]
        return JsonResponse({'message': f'설문조사 결과를 성공적으로 받았습니다. 관심사항: {interests}'})
'''
def calculate_distance(user_location, store_location):
    x_diff = user_location[0] - store_location[0]
    y_diff = user_location[1] - store_location[1]
    
    return math.sqrt(x_diff**2 + y_diff**2)

stores = [
    {"name": "나이키", "location": (37.5665, 126.9780), "category": "패션"},
    {"name": "KBO", "location": (34.5665, 12.9780), "category": "야구"},
    {"name": "블랙핑크", "location": (2.523665, 1263.9780), "category": "음악"},
    {"name": "파이참", "location": (2987.5665, 16.9780), "category": "IT"},
    {"name": "롤", "location": (210039.5665, 209.9780), "category": "게임"},
    {"name": "유럽 여행", "location": (3733.5665, 1216.9780), "category": "여행"},
    {"name": "아디다스", "location": (0.5665, 47.9780), "category": "패션"},
    {"name": "엽떡", "location": (3991.5765, 3.9880), "category": "음식"},
    {"name": "시몬스", "location": (1.5865, 1.9980), "category": "가구"},
]

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


#todo 프론트에서 설문조사 완료한 데이터 가져오기
# //  코드 내부 팀 주제와 기능에 맞게 수정하기