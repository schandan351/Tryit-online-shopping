from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()

class GuestForm(forms.Form):
    email=forms.EmailField()




class ContactForm(forms.Form):
    full_name=forms.CharField(max_length=20,widget=forms.TextInput(attrs=
        {
            "class":"form-control","placeholder":"your full name"
        }
    ))
    email=forms.EmailField(widget=forms.TextInput(attrs=
    {
        "class":"form-control","placeholder":"your email"
    }
    ))
    text=forms.CharField(widget=forms.Textarea(attrs=
    {
        "class":"form-control","placeholder":"your text"
    }
    ))
 


    def clean_email(self):
        email=self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("email has to be gamil.com")
        return email

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class":"form-control","placeholer":"enter your password"
        }
    ))


class RegisterForm(forms.Form):
    username=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is already taken")
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is already taken")
        return email


    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')
        if password2!=password:
            raise forms.ValidationError("password must be same")
        return data
