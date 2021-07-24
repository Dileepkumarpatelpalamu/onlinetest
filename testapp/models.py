from django.db import models
from django.db.models.fields.files import ImageField
from datetime import date, timedelta
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return "%s"%(self.name)
    @staticmethod
    def get_category():
        return Category.objects.all()

class Question(models.Model):
    name = models.TextField()
    option_A = models.CharField(max_length=150)
    option_B = models.CharField(max_length=150)
    option_C = models.CharField(max_length=150)
    option_D = models.CharField(max_length=150)
    image = models.ImageField(upload_to='questions',blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return "%s"%(self.name)
    @staticmethod
    def get_question(cat_id=None):
        if cat_id is None:
            return Question.objects.all().order_by('id')
        else:
            return Question.objects.filter(category=cat_id).order_by('id')
        
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=400)
    def __str__(self):
        return "%s %s %s %s %s"%(self.first_name,self.last_name,self.email,self.phone,self.password)
    @staticmethod
    def validate_email(email):
        if (Student.objects.filter(email=email)):
            return True
        return False
    @staticmethod
    def validate_password(email):
        return Student.objects.filter(email=email).values_list('password')[0][0]
    @staticmethod
    def IsExits(email):
        if Student.objects.filter(email=email).count():
            return True
        return False
    @staticmethod
    def get_student(email):
        return Student.objects.get(email=email)

class UserProfile(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users')
    @staticmethod
    def get_image(email):
        try:
            user =Student.objects.get(email=email)
            return UserProfile.objects.filter(student_id=user.id).last()
        except:
            return None 
class StudentAnswer(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=150,blank=True,default=False)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    def __str__(self):
        return "%s %s"%(self.question,self.answer)
    @staticmethod
    def answer_select(email):
        dt = date.today()
        usr=Student.objects.get(email=email)
        anslist=StudentAnswer.objects.filter(student_id=usr.id,date=dt).values('question','answer')
        stu_ans =[(int(i['question']),i['answer'])for i in anslist]
        pre_ans = Answer.objects.all().values('question_id','answer')
        correct_ans = [(i['question_id'],i['answer']) for i in pre_ans]
        stu_ans,correct_ans = dict(stu_ans),dict(correct_ans)
        correct,wrong = 0,0
        for k,v in stu_ans.items():
            if v == correct_ans[k]:
                correct +=1
            else:
                wrong +=1
        return correct,wrong
    @staticmethod
    def valid_date(id,dt):
        return StudentAnswer.objects.filter(student_id=id,date=dt)
class StudentReportCard(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    total_question = models.IntegerField()
    wrong_answer = models.IntegerField()
    total_atempt = models.IntegerField()
    full_marks = models.FloatField()
    obtained_marks = models.FloatField()
    persentage = models.FloatField()
    remark = models.CharField(max_length=100,blank=True)
    date = models.DateField()
    def __str__(self):
        return "%s"%(self.student)
    @staticmethod
    def save_report(**kwargs):
        print(kwargs)
        dt = date.today()
        stuans=StudentAnswer.objects.filter(student_id=kwargs['id']).last()
        stu_date = stuans.date + timedelta(days=1)
        if dt == stu_date:
            if not StudentReportCard.objects.filter(id=kwargs['id'],date=dt).count():
                stu=StudentReportCard(kwargs)
                stu.date= dt
                stu.save()


class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=150)
    def __str__(self):
        return "%s"%(self.answer)