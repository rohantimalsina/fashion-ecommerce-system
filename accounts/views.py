from base64 import urlsafe_b64decode
from lib2to3.pgen2.tokenize import generate_tokens
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from elite import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.template import loader
from store.models import Detail




def signup(request):

    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists, try other usernames")

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")

        if len(username)>12:
            messages.error(request, "Username must be under 12 characters")

        if password != password2:
            messages.error(request, "Passwords do not match") 

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")           


        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Elite Store Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Elite Store!! We have sent you a confirmation email, please confirm your email address."        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Elite Store - Login!!"
        message2 = render_to_string('accounts/email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
            
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
    details=Detail.objects.all().order_by('-id')
        
    return render(request, "accounts/signup.html",{'details':details})

def activate(request,uidb64,token):
    details=Detail.objects.all().order_by('-id')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'accounts/activation_failed.html',{'details':details})


 
 

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in successfully")
            
            return redirect('home')

           

        else:
            messages.error(request, "Username not found.")
            return redirect('signin')

    details=Detail.objects.all().order_by('-id')      

    return render(request, "accounts/login.html",{'details':details})

def signout(request):
    logout(request)
    return redirect('signin')

def myaccount(request):
    details=Detail.objects.all().order_by('-id')

    return render(request, "accounts/myaccount.html",{'details':details}) 







       


