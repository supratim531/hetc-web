import datetime
from django.db import models
from django.contrib.auth.models import User


class Detail(models.Model):
    total_questions = models.CharField(null=True, blank=True, max_length=5)
    registration_start_date = models.DateField()
    registration_last_date = models.DateField()
    exam_start_date = models.DateField()
    exam_start_time = models.TimeField()
    exam_end_time = models.TimeField()


class Student(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    gurdian_name = models.CharField(max_length=200, blank=True, null=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=11, blank=True, null=True)
    whatsapp = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    school_college_name = models.CharField(max_length=1000, blank=True, null=True)
    passing_year_12 = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    pure_science_combo = models.CharField(max_length=10, blank=True, null=True)
    board_name = models.CharField(max_length=50, blank=True, null=True)
    appeared_wbjee_jeeMain = models.CharField(null=True, blank=True, max_length=10)
    preferred_stream = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    last_seen = models.CharField(max_length=10, blank=True, null=True, default='00:00')
    exam_status = models.BooleanField(default=False)
    student_feedback = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.full_name).replace(' ', '-') + '-' + str(self.user_id)


class Question(models.Model):
    ques_no = models.IntegerField(primary_key=True)
    ques = models.TextField()
    opt1 = models.CharField(max_length=1000)
    opt2 = models.CharField(max_length=1000)
    opt3 = models.CharField(max_length=1000)
    opt4 = models.CharField(max_length=1000)
    opt_ans = models.CharField(max_length=10)
    neg_marks = models.IntegerField(default=0)
    pos_marks = models.PositiveIntegerField(default=0)
    ques_type = models.CharField(null=True, blank=True, max_length=1000)
    image_name = models.CharField(null=True, blank=True, max_length=1000)

    def __str__(self):
        if self.ques == '': return f"{self.ques_no}-" + str(self.image_name)
        else: return f"{self.ques_no}-" + str(self.ques).replace(' ', '_')


class Result(models.Model):
    user = models.CharField(max_length=100)
    total_marks = models.IntegerField(default=0)
    exam_status = models.BooleanField(default=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + '-' + str(self.total_marks)


class Choose(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    user = models.CharField(max_length=100, default=None)
    question_number = models.CharField(max_length=5)
    selected_option = models.CharField(max_length=5)

    def __str__(self):
        return self.user
