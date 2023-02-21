from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile


def index(request):
    return render(request,'index.html')

def reg(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('reg')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'User name taken')
                return redirect('reg')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,user_id=user_model.id)
                new_profile.save()
                return redirect('reg')
        else:
            messages.info(request,'password not matching')
            return redirect('reg')
    else:    
       return render(request,'reg.html')    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid user')
            return redirect('login')
    else:        
        return render(request,'login.html')
