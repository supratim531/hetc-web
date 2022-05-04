import json
import datetime

from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from .models import *
from .helper import timer, is_exam, user_id, hashed2, verified, eliminate, last_seen, date_over, time_ahead, user_password, is_exam_running, record_is_duplicate

def home(request):
    date_ob = Detail.objects.get(pk=1)
    last_date = date_ob.registration_last_date.strftime("%d-%B-%Y")
    start_date = date_ob.registration_start_date.strftime("%d-%B-%Y")

    dictt = {
        'last_date': last_date,
        'start_date': start_date,
        'date_over': date_over(Detail),
        'ahead_of_time': time_ahead(Detail)
    }

    return render(request, 'candidate/home.html', {'dictt': dictt})

def contact(request):
    dictt = {
        'date_over': date_over(Detail),
        'ahead_of_time': time_ahead(Detail)
    }

    return render(request, 'candidate/contact.html', {'dictt': dictt})

def register(request):
    dictt = {
        'date_over': date_over(Detail),
        'ahead_of_time': time_ahead(Detail)
    }

    if request.user.is_authenticated or date_over(Detail) or time_ahead(Detail):
        return redirect('home')

    if request.method == 'POST':
        fname = str(request.POST.get('fname')).upper()
        lname = str(request.POST.get('lname')).upper()
        gurdian = str(request.POST.get('gurdian')).upper()

        date = request.POST.get('date')
        year = request.POST.get('year')
        month = request.POST.get('month')

        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')
        email = str(request.POST.get('email')).lower()

        if record_is_duplicate(fname, lname, gurdian, email):
            messages.error(request, "Some information are there which already exists in our records (may occur duplicate)")
            return render(request, 'candidate/register.html', {'dictt': dictt})

        else:
            instu = request.POST.get('inst')
            board = request.POST.get('board')
            status = request.POST.get('status')
            entrance = request.POST.get('entrance')
            address = str(request.POST.get('address')).upper()

            userid = user_id(fname)
            password = user_password(date, month, year)
            date_of_birth = password[0:2] + '/' + password[2:4] + '/' + password[4:10]

            student = Student(first_name=fname, last_name=lname, user_id=userid,
            date_of_birth=date_of_birth, gurdian_name=gurdian, contact=phone, whatsapp=whatsapp,
            email=email, address=address, school_college_name=instu, appearing_passed_12=status,
            board_name=board, appeared_wbjee_jeeMain=entrance, created_at=datetime.datetime.now())
            student.save()

            subject = "Thank You for registration"
            body = f"Your user name is {userid} and your password is {password}"
            messages.success(request, 'Your Registration is completed. Check Your Email To get User ID and Password')

            mail_sender = "utsavpokemon9000chatterjee"
            send_mail(subject, body, mail_sender, [email], fail_silently=False)

            user = User.objects.create_user(userid, email, password)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()

    return render(request, 'candidate/register.html', {'dictt': dictt})

def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.warning(request, 'Wrong Username or Password')

    return render(request, 'candidate/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@csrf_exempt
@login_required(login_url='login')
def exam_authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and username == request.user.username:
            encoded_username = hashed2(username).decode('UTF-8')
            return redirect(f'auth-user/exam/{encoded_username}')
        else:
            messages.warning(request, 'Wrong Username or Password')

    return render(request, 'candidate/exam_auth.html')

@api_view(['GET', 'POST'])
def api(request, userid):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        select = "None"
        index = str(request.data['index'])
        ob = Choose.objects.filter(user=userid)

        if ob.exists():
            selected = ob.filter(question_number=index).values('selected_option')

            if selected.exists():
                select = selected[0]['selected_option']

        ques_ob = Question.objects.get(pk=int(index))
        question = {
            "id": index,
            "ques": ques_ob.ques,
            "opt1": ques_ob.opt1,
            "opt2": ques_ob.opt2,
            "opt3": ques_ob.opt3,
            "opt4": ques_ob.opt4,
            "selected_option": select
        }

        data = json.dumps(question)
        return Response(data)

    return Response({"status": 200})

def exam(request, userid):
    user = request.user

    if request.method == 'GET':
        if is_exam_running(Detail):
            userid = bytes(userid, 'UTF-8')

            if Student.objects.filter(user_id=user).values('exam_status')[0]['exam_status'] == True:
                messages.warning(request, f'{user.first_name} {user.last_name} You have already give your examination')
                return render(request, 'candidate/exam_auth.html')

            if verified(user.username, userid):
                field_name = 'total_questions'
                obj = Detail.objects.first()
                field_object = Detail._meta.get_field(field_name)
                total_questions = getattr(obj, field_object.attname)

                date_ob = Detail.objects.get(pk=1)
                start_time = str(date_ob.exam_start_time)
                start_date = date_ob.exam_start_date.strftime("%B %d, %Y")
                rem_days = str((date_ob.exam_start_date - datetime.date.today()).days) + " days"

                dictt = {
                    'start_date': start_date,
                    'start_time': start_time,
                    'is_exam': is_exam(Detail),
                    'remaining_days': rem_days,
                    'exam_duration': timer(Detail),
                    'number_of_questions': eliminate(total_questions)
                }
                return render(request, 'candidate/exam.html', {'dictt': dictt})

            else:
                return render(request, 'candidate/exam_auth.html')

        elif Student.objects.filter(user_id=user).values('exam_status')[0]['exam_status'] == True:
                messages.warning(request, f'{user.first_name} {user.last_name} You have already give your examination')
                return render(request, 'candidate/exam_auth.html')

        else:
            messages.warning(request, f'{user.first_name} {user.last_name} Time of your examination is over')
            return render(request, 'candidate/exam_auth.html')

    elif request.method == 'POST':
        if request.headers['Content-Length'] == '14':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            exam_stat = (body['msg'])
            Student.objects.filter(user_id=userid).update(exam_status=exam_stat)

            ques_ob = Question.objects.all()
            ans_ob = Choose.objects.filter(user=userid)

            total_marks = 0
            for i in ans_ob:
                for j in ques_ob:
                    if j.ques_no == int(i.question_number):
                        if(j.opt_ans == i.selected_option):
                            total_marks += j.pos_marks

            result_ob = Result(user=userid, author=user, total_marks=total_marks)
            print("Result accepted")
            result_ob.save()

        elif request.headers['Content-Length'] == '63':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            Student.objects.filter(user_id=userid).update(last_seen=last_seen())

        else:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            index = str(body['index'])
            option = str(body['option'])
            print("Pair:", index, '-', option)

            if index != '0':
                opt_ob = Choose.objects.filter(user=userid)

                if opt_ob.exists():
                    ob = opt_ob.filter(question_number=index)

                    if ob.exists():
                        ob.update(selected_option=option)
                    else:
                        Choose.objects.create(author=request.user, user=userid, question_number=index, selected_option=option)

                else:
                    Choose.objects.create(author=request.user, user=userid, question_number=index, selected_option=option)

    return render(request, 'candidate/exam.html')

def exam_end(request, user):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        feedback = (body['option'])
        Student.objects.filter(user_id=user).update(student_feedback=feedback)
        return redirect('home')

    if user != request.user.username:
        return redirect('home')

    if Student._meta.get_field('student_feedback').value_from_object(Student.objects.get(user_id=user)) is not None:
        return redirect('home')

    user_ob = Student.objects.get(user_id=user)
    exam_status = Student._meta.get_field('exam_status').value_from_object(user_ob)

    if exam_status == False: exam_is_on = True
    else: exam_is_on = False

    if not exam_is_on:
        return render(request, 'candidate/exam_end.html')

    else:
        return redirect('home')
