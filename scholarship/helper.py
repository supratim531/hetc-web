import random
import hashlib
import datetime

from .models import Student

from hmac import compare_digest
from django.contrib.auth.models import User

def user_id(username):
    while True:
        user_id = str(username).upper() + str(random.randint(1875, 9370))
        if User.objects.filter(username=user_id):
            continue
        else:
            return user_id

def user_password(date, month, year):
    dd, mm, yyyy = str(date), str(month), str(year)

    if len(dd) == 1:
        dd = '0' + dd
    if len(mm) == 1:
        mm = '0' + mm

    return dd + mm + yyyy

def eliminate(digit):
    one_digit = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
    return int(digit.replace('0', '')) if str(digit) in one_digit else int(digit)

def is_exam(Details):
    ob = Details.objects.first()

    if datetime.date.today() < ob.exam_start_date:
        return False

    if datetime.date.today() == ob.exam_start_date:
        if datetime.datetime.now().time() < ob.exam_start_time:
            return False

    return True

def hashed(string):
    hashed_string = hashlib.sha256(string.encode('UTF-8')).hexdigest()
    return hashed_string

def hashed2(string):
    string = bytes(string, 'UTF-8')
    hash = hashlib.blake2b(digest_size=16, key=string)
    hash.update(string)
    return hash.hexdigest().encode('UTF-8')

def verified(string, hashed_string):
    string = hashed2(string)
    return compare_digest(string, hashed_string)

def last_seen():
    c_hour = datetime.datetime.now().strftime("%H")
    c_minute = datetime.datetime.now().strftime("%M")
    return str(c_hour) + ':' + str(c_minute)

def is_exam_running(Details):
    ob = Details.objects.first()

    if datetime.date.today() == ob.exam_start_date:
        if datetime.datetime.now().time() > ob.exam_end_time:
            return False

    if datetime.date.today() > ob.exam_start_date:
        return False

    return True

def date_over(Details):
    ob = Details.objects.first()

    if datetime.date.today() <= ob.registration_last_date:
        return False

    else:
        return True

def time_ahead(Details):
    ob = Details.objects.first()

    if datetime.date.today() < ob.registration_start_date:
        return True

    else:
        return False

def record_is_duplicate(fname, lname, gurdian, email):
    if Student.objects.filter(gurdian_name=gurdian):
        if Student.objects.filter(first_name=fname) and Student.objects.filter(last_name=lname):
            return True

    if Student.objects.filter(email=email):
        return True

    return False

def timer(Details):
    ob = Details.objects.first()
    end_time = datetime.datetime.combine(datetime.date(1, 1, 1), ob.exam_end_time)
    curr_time = datetime.datetime.combine(datetime.date(1, 1, 1), datetime.datetime.now().time())
    return (end_time - curr_time).seconds

def handle_upload_file(file):
    with open(f'./media/{file.name}', "wb+") as fPtr:
        for chunk in file.chunks():
            fPtr.write(chunk)
