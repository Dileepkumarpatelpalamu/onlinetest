"""onlinetest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from onlinetest.settings import MEDIA_ROOT
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from testapp.views import Home,Login,Signup, get_answer,get_success, getquestion,logout,upload_photo,resultspage
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(),name='homepage'),
    path('login/',Login.as_view(),name="login"),
    path('signup/',Signup.as_view(),name="signup"),
    path('profile/',get_success,name='profile'),
    path('photo/',upload_photo,name='upload_photo'),
    path('getquestion/',getquestion,name='getquestion'),
    path('getanswer/',get_answer,name='getanswer'),
    path('resultpage/',resultspage,name="resultpage"),
    path('logout/',logout,name='logout'),

] + static(settings.MEDIA_URL,document_root=MEDIA_ROOT)
