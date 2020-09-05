from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import requests
# from .models import UserData


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            # to_email = form.cleaned_data.get('email')
            # name= form.cleaned_data.get('username')
            # pass1=form.cleaned_data.get('password1')
            # print(name)
            # print(pass1)
            # response = requests.get("http://api.quickemailverification.com/v1/verify?email="+to_email+"&apikey=519847e067dab09cd0a1c56e334105fffa8dd9793a96ccc61c808db1ae7f")
            # result=response.json()

            # if (result['did_you_mean']=='' and result['result']=="valid"):
                # print("valid")
                # userdata=UserData.objects.create(email=to_email,name=name,password=pass1)
            user.save()
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            try:
                u=User.objects.get(username=name)
                u.delete()
            except User.DoesNotExist:
                return HttpResponse('The email given is invalid please check it ')
            except Exception as e:
                return render(request, 'signup.html', {'form': form})
            return HttpResponse('The email given is invalid please check it ')



    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        # return render(request, 'login.html')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return render(request, 'login.html', {'form': form})
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    
    if request.method =='POST':
        loginusername = request.POST['uname']
        loginpassword = request.POST['psw']   

        user = authenticate(request,username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            # messages.success(request,'Your Account has been Successfully logged in')
            return redirect('student')
        else:
            # messages.error(request,'please try again later')
            return render(request,'login.html')
	
		
    return render(request,'login.html')
def student(request):
    return render(request, 'student.html')
