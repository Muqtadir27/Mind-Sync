"""
URL configuration for mindsync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from home.views import homepage
from about.views import about
from contact.views import Contact
from yus.views import whyus
from mindsync.views import mainms
from Student.views import login,signup,mailrvry
from main.views import home,detect_face_emotion,detect_emotion,text_chat,face_emotion_view,get_content_by_emotion
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name="home"),
    path('About/',about,name="About"),
    path('Contact/',Contact,name="Contact"),
    path('Why-us/',whyus,name='Why-us'),
    path('MindSync/',mainms,name='MindSync'),
    path('login/', login, name='Login'),
    path('Sign-Up/',signup,name="Signup"),
    path('Recovery/',mailrvry,name="recovery"),
    path('home/', home, name='Studenthome'),
    path('detect-face-emotion/', detect_face_emotion, name='detect-face-emotion'),
    path('text/', text_chat, name='text_chat'),
    path('detect_emotion/', detect_emotion, name='detect_emotion'),
    path('face/', face_emotion_view, name='face_emotion'),
    path('api/content/',get_content_by_emotion, name='get_content'),
]
