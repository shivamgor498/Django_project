"""proj1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from app1 import views
urlpatterns = [
    path('',views.default),
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('student_dash/',views.stud_dash,name='stud_dash'),
    path('librarian_dash/',views.lib_dash,name='lib_dash'),
    path('logout/',views.logout),
    path('book_details/',views.book_details),
    path('add_books/',views.add_books),
    path('request_books/',views.request_books),
    path('profile/',views.profile),
    path('home/',views.home),
    path('search/',views.search),
    path('currentBookings/',views.currentBookings),
    path('pdf/',views.pdf_generator),
]
