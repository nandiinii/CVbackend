from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (BlacklistTokenView,LoggedInUserView,RegisterView,DetailAddView,
                    ResumeScannerView,IndResumeView)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.conf.urls.static import static
from . import views
from django.conf import settings


router=DefaultRouter()
router.register('register',RegisterView,basename='register')
router.register('detail-add',DetailAddView,basename='detail-add')


my_viewset = ResumeScannerView.as_view({
    'post': 'create',
    'create' : 'get',
})

urlpatterns = [
    path('',include(router.urls)),
    path('api/token/',TokenObtainPairView.as_view(),name="token_obtain"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="refresh_token"),
    path('api/token/blacklist/',BlacklistTokenView.as_view(),name="blacklist"),
    path('current-user/', LoggedInUserView.as_view(), name='currentuser'),
    path('resume-analyze/', my_viewset, name = "resume_analyze"),
    path('resume-analyze/<int:pk>/',IndResumeView.as_view(), name = "resume_analyze_ind"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

