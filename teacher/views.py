import datetime

from scholarship.models import *
from django.contrib import messages
from rest_framework.response import Response
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from scholarship.helper import eliminate, handle_upload_file

# Create your views here.

def set_question(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    obj = Question.objects.last()
    field_object = Question._meta.get_field('ques_no')
    field_value = field_object.value_from_object(obj)
    print(field_value, type(field_value))

    if request.method == 'POST':
        obj = Question.objects.last()
        field_object = Question._meta.get_field('ques_no')
        field_value = field_object.value_from_object(obj)

        ques_no = eliminate(request.POST.get('quesno'))
        ques = request.POST.get('ques')
        opta = request.POST.get('opta')
        optb = request.POST.get('optb')
        optc = request.POST.get('optc')
        optd = request.POST.get('optd')
        correct = str(request.POST.get('correct')).lower()
        marks = eliminate(request.POST.get('marks'))

        # handle exception
        if correct != 'a' and correct != 'b' and correct != 'c' and correct != 'd':
            dictt = { "total": Question.objects.count() }
            messages.error(request, f'Please set correct option either a, b, c or d')
            return render(request, 'teacher/question.html', {'dictt': dictt})

        if Question.objects.filter(ques_no=ques_no):
            dictt = { "total": Question.objects.count() }
            messages.error(request, f'Question number {ques_no} is already used by another question')
            return render(request, 'teacher/question.html', {'dictt': dictt})

        if ques_no - field_value != 1:
            dictt = { "total": Question.objects.count() }
            messages.error(request, f'Please add question number {field_value + 1} (last added question no. {field_value})')
            return render(request, 'teacher/question.html', {'dictt': dictt})

        if Question.objects.filter(ques=ques):
            if Question.objects.filter(opt1=opta) and Question.objects.filter(opt2=optb) and Question.objects.filter(opt3=optc) and Question.objects.filter(opt4=optd):
                dictt = { "total": Question.objects.count() }
                messages.error(request, 'This question is already added')
                return render(request, 'teacher/question.html', {'dictt': dictt})
        # handle exception

        question_ob = Question(ques_no=ques_no, ques=ques, opt1=opta, opt2=optb, opt3=optc, opt4=optd,
        opt_ans=correct, pos_marks=marks, neg_marks=(marks * -1))
        question_ob.save()

        messages.success(request, 'One question successfully added')

    dictt = {
        "total": Question.objects.count()
    }

    return render(request, 'teacher/question.html', {'dictt': dictt})

def set_schedule(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        ques_no = int(request.POST.get('quesno'))
        exam_end = str(request.POST.get('examend'))
        exam_date = str(request.POST.get('examdate'))
        exam_start = str(request.POST.get('examstart'))
        reg_last_date = str(request.POST.get('reglastdate'))
        reg_start_date = str(request.POST.get('regstartdate'))

        handle_upload_file(request.FILES['pdf'])
        exam_end = datetime.datetime.strptime(exam_end, '%H:%M').time()
        exam_start = datetime.datetime.strptime(exam_start, '%H:%M').time()
        exam_date = datetime.datetime.strptime(exam_date, '%Y-%m-%d').date()
        reg_last_date = datetime.datetime.strptime(reg_last_date, '%Y-%m-%d').date()
        reg_start_date = datetime.datetime.strptime(reg_start_date, '%Y-%m-%d').date()

        print(ques_no, type(ques_no))
        print(reg_start_date, type(reg_start_date))
        print(reg_last_date, type(reg_last_date))
        print(exam_date, type(exam_date))
        print(exam_start, type(exam_start))
        print(exam_end, type(exam_end))
        print(request.FILES['pdf'], type(request.FILES['pdf']))

        Detail.objects.update(total_questions=ques_no, registration_start_date=reg_start_date,
        registration_last_date=reg_last_date, exam_start_date=exam_date, exam_start_time=exam_start,
        exam_end_time=exam_end)

        messages.success(request, 'Exam Schedule Successfully Updated')

    return render(request, 'teacher/schedule.html')

@csrf_exempt
@login_required(login_url='login')
def students(request):
    if request.user.is_superuser:
        return render(request, 'teacher/student_records.html')

    else:
        messages.error(request, 'You have not administrative permission')
        return render(request, 'candidate/login.html')

@api_view(['GET', 'POST'])
def fetch_student_records(request):
    if request.method == 'GET':
        if not request.user.is_superuser:
            return redirect('home')

        dataset = []
        usernames = []

        for user in Student.objects.all():
            usernames.append(user.user_id)

        for username in usernames:
            result_ob = Result.objects.filter(user=username)
            student = Student.objects.filter(user_id=username)

            if result_ob.exists():
                total_marks = result_ob.values('total_marks')

            else:
                total_marks = [{'total_marks': "None"}]

            data = {
                "user_id": username,
                "first_name": student.values('first_name'),
                "last_name": student.values('last_name'),
                "date_of_birth": student.values('date_of_birth'),
                "gurdian_name": student.values('gurdian_name'),
                "contact": student.values('contact'),
                "whatsapp": student.values('whatsapp'),
                "email": student.values('email'),
                "address": student.values('address'),
                "institute_name": student.values('school_college_name'),
                "appearing_passed_12": student.values('appearing_passed_12'),
                "board_name": student.values('board_name'),
                "appeared_wbjee_jeeMain": student.values('appeared_wbjee_jeeMain'),
                "total_marks": total_marks
            }

            dataset.append(data)

        return Response(dataset)

    return Response({'status': 200})
