from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()
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