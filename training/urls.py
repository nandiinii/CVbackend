from django.urls import path, include
from .views import PersonalityViewSet
from rest_framework.routers import DefaultRouter



router=DefaultRouter()
my_viewset = PersonalityViewSet.as_view({
    'post': 'predict_personality',
    'create' : 'get',
})

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', my_viewset, name='predict'),
]
