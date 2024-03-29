from django.urls import path, include
from .views import PersonalityViewSet,AptitudeTest,QuestionListView,ScoreView
from rest_framework.routers import DefaultRouter



router=DefaultRouter()
my_viewset = PersonalityViewSet.as_view({
    'post': 'predict_personality',
    'create' : 'get',
    'get' : 'retrieve'
})

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', my_viewset, name='predict'),
    path('predict/<int:pk>/', my_viewset, name='predict-detail'),
    path('aptitude/', AptitudeTest.as_view()),
   path('question/<int:pk>',QuestionListView.as_view()),
   path('score/',ScoreView.as_view())
]
