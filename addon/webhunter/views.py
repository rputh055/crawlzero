from django.shortcuts import render, redirect
from webhunter.forms import UserForm, FileUploadModelForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from .models import File
from .scrap import Scraper

# Create your views here.
scraper_obj = Scraper()

def index(request):
    return render(request,'webhunter/index.html')
@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'webhunter/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'webhunter/login.html', {})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            infile = form.save(commit=False)
            infile.user = request.user
            infile.save()
            outfile = scraper_obj.parser(request.FILES['file'])
            infile.delete()
            response = HttpResponse(outfile, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="updated.xls"'
            return response
            #return render(request, 'webhunter/login.html', {})
        else:
            return HttpResponse('Upload a csv or excel file')
    else:
        form = FileUploadModelForm()

        
    return render(request, 'webhunter/upload.html', {'form': form})