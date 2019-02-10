from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from django.utils.http import is_safe_url
from .forms import LoginForm,RegisterForm,GuestForm
from .models import GuestEmail
# Create your views here.

# guest view
def guest_login_view(request):
    guestform=GuestForm(request.POST or None)
    context={
        "login":GuestForm,
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if guestform.is_valid():
        email=guestform.cleaned_data.get("email")
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id

        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register")
    return redirect("/register")



def login_page(request):
    loginform=LoginForm(request.POST or None)
    context={
        "login":loginform,
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if loginform.is_valid():
        print(loginform.cleaned_data)
        # context['form']:LoginForm()
        username=loginform.cleaned_data.get("username")
        password=loginform.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/products")
        else:
            print("error")
    return render(request,"auth/login_page.html",context)

User=get_user_model()
def register_page(request):
    register_form=RegisterForm(request.POST or None)
    context={
        'register':register_form,
    }
    if register_form.is_valid():
        print(register_form.cleaned_data)
        username=register_form.cleaned_data.get('username')
        email=register_form.cleaned_data.get('email')
        password=register_form.cleaned_data.get('password')
        new_user=User.objects.create_user(username,email,password)
        print(new_user)
    return render(request,"auth/register_page.html",context)