import datetime

from scholarship.models import *
from django.contrib import messages
from rest_framework.response import Response
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from scholarship.helper import eliminate, handle_upload_file, handle_image_question

SAFETY_CALCULATION = True

def set_question(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        total_ques = 0
        image = "NoImage"

        ques = request.POST.get('ques')
        opta = request.POST.get('opta')
        optb = request.POST.get('optb')
        optc = request.POST.get('optc')
        optd = request.POST.get('optd')
        boolans = request.POST.get('boolans')
        correct = request.POST.get('correct')
        questype = request.POST.get('questype')
        marks = eliminate(request.POST.get('marks'))

        if questype == "Boolean":
            correct = boolans
            opta, optb, optc, optd = ("True", "False", '', '')

        elif questype == "Image" or questype == "Normal":
            if questype == "Image": ques = ''

            try:
                image = str(request.FILES['image'])
                handle_image_question(request.FILES['image'])

            except:
                pass

            # handle normal exception
            try:
                if correct != 'a' and correct != 'b' and correct != 'c' and correct != 'd':
                    dictt = { "total": Question.objects.count() }
                    messages.error(request, f'Please set correct option either a, b, c or d')
                    return render(request, 'teacher/question.html', {'dictt': dictt})

            except:
                pass
            # handle normal exception

        # DEBUG
        print("ques:", ques)
        print("opta:", opta)
        print("optb:", optb)
        print("optc:", optc)
        print("optd:", optd)
        print("marks:", marks)
        print("boolans:", boolans)
        print("correct:", correct)
        print("questype:", questype)
        # DEBUG

        Question(ques_no=int(Question.objects.count()) + 1, ques=ques, opt1=opta, opt2=optb,
        opt3=optc, opt4=optd, opt_ans=correct, pos_marks=marks, neg_marks=(marks * -1), ques_type=questype,
        image_name=image).save()

        messages.success(request, 'One question successfully added')

    try:
        total_ques = Question.objects.count()

    except:
        pass

    dictt = { "total": total_ques }

    return render(request, 'teacher/question.html', {'dictt': dictt})

def set_schedule(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        exam_end = str(request.POST.get('examend'))
        if exam_end != '':
            exam_end = datetime.datetime.strptime(exam_end, '%H:%M').time()
            Detail.objects.update(exam_end_time=exam_end)

        exam_start = str(request.POST.get('examstart'))
        if exam_start != '':
            exam_start = datetime.datetime.strptime(exam_start, '%H:%M').time()
            Detail.objects.update(exam_start_time=exam_start)

        exam_date = str(request.POST.get('examdate'))
        if exam_date != '':
            exam_date = datetime.datetime.strptime(exam_date, '%Y-%m-%d').date()
            Detail.objects.update(exam_start_date=exam_date)

        reg_last_date = str(request.POST.get('reglastdate'))
        if reg_last_date != '':
            reg_last_date = datetime.datetime.strptime(reg_last_date, '%Y-%m-%d').date()
            Detail.objects.update(registration_last_date=reg_last_date)

        reg_start_date = str(request.POST.get('regstartdate'))
        if reg_start_date != '':
            reg_start_date = datetime.datetime.strptime(reg_start_date, '%Y-%m-%d').date()
            Detail.objects.update(registration_start_date=reg_start_date)

        try:
            handle_upload_file(request.FILES['pdf'])

        except:
            pass

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

        global SAFETY_CALCULATION
        ob = Detail.objects.first()

        if datetime.date.today() == ob.exam_start_date and datetime.datetime.now().time() > ob.exam_end_time and SAFETY_CALCULATION:
            SAFETY_CALCULATION = False
            print("\nResult Calculate")

            for user in User.objects.all():
                if Choose.objects.filter(user=user.username).exists():
                    if not Result.objects.filter(user=user.username).exists():
                        Student.objects.filter(user_id=user.username).update(exam_status=True)

                        ques_ob = Question.objects.all()
                        ans_ob = Choose.objects.filter(user=user.username)

                        total_marks = 0
                        for i in ans_ob:
                            for j in ques_ob:
                                if j.ques_no == int(i.question_number):
                                    if(j.opt_ans == i.selected_option):
                                        total_marks += j.pos_marks

                        result_ob = Result(user=user.username, author=user, total_marks=total_marks)
                        print(f"Result calculated for user {user}\n")
                        result_ob.save()

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
                total_marks = [{'total_marks': "Not Attended"}]

            data = {
                "user_id": username,
                "full_name": student.values('full_name'),
                "date_of_birth": student.values('date_of_birth'),
                "contact": student.values('contact'),
                "email": student.values('email'),
                "institute_name": student.values('school_college_name'),
                "last_seen": student.values('last_seen'),
                "total_marks": total_marks
            }

            dataset.append(data)

        return Response(dataset)

    return Response({'status': 200})
