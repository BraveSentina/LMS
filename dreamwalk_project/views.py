from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse

from management.models import *

def homepage_page(request):
    context = {}
    return render(request,'homepage.html',context)

def login_page(request):
    if request.user.is_authenticated:
        do_logout(request)

    context = {}
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        print("Username: ",username," password: ",password)
        user = authenticate(username=username,password=password)

        print("User is : ",user)
        if user is not None:
            if user.is_active:
                login(request,user)
                print("Login success")

                if user.is_superuser: # If admin, take to administrator dashboard
                    return redirect('administrator:dashboard_page')
                if user.is_faculty:
                    return redirect('faculty:dashboard_page')
                if user.is_student:
                    return redirect('student:dashboard_page')
        else:
            print("It is none")
            context = {
                'error':'error'
            }
    return render(request,'login.html',context)










def do_logout(request):
    logout(request)
    return redirect('login_page')