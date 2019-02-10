from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from .forms import ContactForm

def home_page(request):
    context={
    "content":"this is about home page",
    }

    if request.user.is_authenticated():
        context["premium_content"]="this is premium content"
    return render(request,"home_page.html",context)



def about_page(request):
    context={
        "title":"this is about page"
    }
    return render(request,"home_page.html",context)



def contact_page(request):
    contactform=ContactForm(request.POST or None)
    context={
        "title":"this is contact page",
        "form":contactform,
    }
    if contactform.is_valid():
        print(contactform.cleaned_data)
    return render(request,"contact/view.html",context)

    