from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('contact/', contact, name='contact'),
    path('api/<str:userid>/', api, name='api'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('server-maintenance/', freeze, name='freeze'),
    path('exam-status/<str:user>/', exam_end, name='exam_end'),
    path('exam-credential/', exam_authentication, name='exam_auth'),
    path('exam-credential/auth-user/exam/<str:userid>/', exam, name='exam'),
    path('activate/<uidb64>/<token>/<details>/', user_verification, name='activate')
]
