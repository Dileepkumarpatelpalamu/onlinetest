from django.contrib import admin
from .models import Category,Question,Answer,Student,StudentAnswer,StudentReportCard,UserProfile
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','name','option_A','option_B','option_C','option_D']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question','answer']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','phone','password'] 

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question','answer','student','date']

@admin.register(UserProfile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['id','student']
@admin.register(StudentReportCard)
class StudentReportCardAdmin(admin.ModelAdmin):
    list_display = ['id','student','total_question','wrong_answer','total_atempt','full_marks','obtained_marks','persentage','remark','date']
