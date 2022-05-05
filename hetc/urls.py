"""hetc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import datetime

from django.conf import settings
from django.contrib import admin
from scholarship.models import Detail
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('scholarship.urls')),
    path('teacher/', include('teacher.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def add_days(days):
    return datetime.timedelta(days=days)

def init_schedule():
    if Detail.objects.count() == 0:
        reg_start_date = datetime.date.today() + add_days(1)
        reg_last_date = datetime.date.today() + add_days(15)
        exam_date = datetime.date.today() + add_days(20)
        exam_start = datetime.time(10, 30, 0)
        exam_end = datetime.time(11, 30, 0)

        ob = Detail(total_questions=0, registration_start_date=reg_start_date,
        registration_last_date=reg_last_date, exam_start_date=exam_date, exam_start_time=exam_start,
        exam_end_time=exam_end)
        ob.save()

        print("Exam Schedule Initialized")
    
    else:
        print("Exam Schedule already exists")

init_schedule()
