from .views import *
from django.urls import path

urlpatterns = [
	path('student-records/', students, name='students'),
	path('set-exam-schedule/', set_schedule, name='set_schedule'),
	path('set-exam-questions/', set_question, name='set_question'),
	path('student-api/', fetch_student_records, name='student_data_api')
]
