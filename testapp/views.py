from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from .forms import PhotoForm
from datetime import date
# Create your views here.
class Home (View):
    def get(self,request):
        cat_id = request.GET.get('cat_id')
        question = Question.get_question(cat_id)
        category = Category.get_category()
        data ={'questions':question,'categorys':category}
        return render(request,'home.html',data)
    def post(self,request):
        pass

class Login(View):
    def get(self,request):
        if request.session.get('email'):
            return redirect('profile')
        return render(request,'login.html')
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not Student.validate_email(email):
            messages.error(request,'Email too wrong..!')
            return redirect('login')
        pass_hash = Student.validate_password(email)
        if check_password(password,pass_hash):
            request.session['email'] = email
            messages.success(request,'You are loggin successfully')
            return redirect('/profile/')
        else:
            messages.error(request,'Email and password too wrong..!')
            return redirect('login')
def get_success(request):
    if not request.session.get('email'):
        return redirect('login')
    category = Category.get_category()
    image = UserProfile.get_image(request.session.get('email'))
    if image :
        user = {'users':Student.get_student(request.session.get('email')),"photo":image.photo.url,'categorys':category}
    else:
        user = {'users':Student.get_student(request.session.get('email')),"photo":None,'categorys':category}
        
    return render(request,'profile.html',user)
def getquestion(request):
    if request.method == 'POST':
        cat_id = request.POST.get('category')
        questions = Question.objects.filter(category_id=cat_id)
        return render(request,'getquestions.html',{'questions':questions})
    else:
        return redirect('/profile/')
def get_answer(request):
    if request.method == 'POST':
        answer = request.POST
        qid =[]
        ans = []
        i = 0
        for item in answer.items():
            if i >0:
                qid.append(int(item[0]))
                ans.append(item[1])
            i +=1
        user = Student.objects.get(email=request.session.get('email'))
        id = user.id 
        dt = date.today()
        if not StudentAnswer.valid_date(id,dt).count():
            for i in range(len(ans)):
                status = StudentAnswer.objects.create(question=qid[i],answer=ans[i],student_id=id)
            messages.success(request,"Answer successfully submited..!")
        else:
            messages.success(request,"You are already submit test so you can't be submit now..!")
        return redirect('/profile/')
def upload_photo(request):
    if request.method == 'GET':
        photo = PhotoForm()
        data ={'data':photo}
        return render(request,'photo.html',data)
    else:
        email = request.session.get('email')
        photo = request.FILES['photo']
        user = Student.objects.get(email=email)
        status = UserProfile.objects.create(student_id=user.id,photo=photo)
        messages.success(request,'Photo Uploaded successfully')
        return redirect('/profile/')
def logout(request):
    if request.session.get('email'):
        request.session.flush()
        messages.success(request,'Your are logged out succefully..!')
        return redirect('login')
    else:
        return redirect('login')
class Signup(View):
    def get(self,request):
        if request.session.get('email'):
            return redirect('profile')
        return render(request,'signup.html')
    def post(self,request):
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if Student.IsExits(email):
            messages.error(request,'Email already exits try another..!')
            return redirect('signup')
        student = Student(first_name=fname,last_name=lname,email=email,phone=phone,password=password)
        student.password= make_password(student.password)
        student.save()
        messages.success(request,'Your email registered successfully..!')
        return redirect('signup')

def resultspage(request):
    if request.method =="GET":
        correct,wrong =StudentAnswer.answer_select(request.session.get('email'))
        total_quest = correct + wrong
        atempt_qest = total_quest
        full_marks = total_quest*5
        marks_obtained= correct*5
        percentage = (marks_obtained/full_marks)*100
        stu_id = Student.get_student(request.session.get('email'))
        id = stu_id.id
        remark = student_remark(percentage)
        report = StudentReportCard.save_report(remark=remark,id=id,total_question=total_quest,wrong_answer=wrong,total_atempt=atempt_qest,percentage=percentage,full_marks=full_marks,marks_obtained=marks_obtained)
        image = UserProfile.get_image(request.session.get('email'))
        if image :
            user = {'users':Student.get_student(request.session.get('email')),"photo":image.photo.url}
        else:
            user = {'users':Student.get_student(request.session.get('email')),"photo":None}
        return render(request,'resultpage.html',user)
def student_remark(percentage):
    if percentage >=80:
        return "Distinct marks on the section. I wish you to better performance."
    elif percentage >=70:
        return "Your marks is good so I wish you!"
    elif percentage >=60:
        return "You need to studying with honesty."
    elif percentage>=45:
        return "You need to hard labourious in life to last to you."
    elif percentage>=30:
        return "You like a fail but you need to hard labourious."
    else:
        return "Sorry! you need to atempt next time..!"


