from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from store.models import UserProfile,Project

class SignUpForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))


    class Meta:

        model=User

        fields=["username","email","password1","password2"]

        widgets={

            "username":forms.TextInput(attrs={"class":"form-control mb-2"}),
            "email":forms.EmailInput(attrs={"class":"form-control mb-2"}),
        }



class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-2"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))        



class UserProfileForm(forms.ModelForm):

    class Meta:

        model=UserProfile

        fields=["bio","profile_pic"]

        widgets={
            "bio":forms.TextInput(attrs={"class":"w-full border p-2 my-3"}),
            "profile_pic":forms.FileInput(attrs={"class":"w-full border  py-2"})
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        exclude=("owner","created_date","updated_date","is_active")

        widgets={
            "title":forms.TextInput(attrs={"class":"w-full border p-3 mb-2"}),
            "description":forms.Textarea(attrs={"class":"w-full border mx-auto p-3 mb-2","rows":5}),
            "tag_objects":forms.SelectMultiple(attrs={"class":"mb-2 w-full"}),
            "thumbnail":forms.TextInput(attrs={"class":"mb-2 w-full"}),
            "game_pic":forms.FileInput(attrs={"class":"mb-2 w-full"}),
            "price":forms.NumberInput(attrs={"class":"w-1/2 mb-2"}),
            "file":forms.FileInput(attrs={"class":"mb-2 w-full border"}),


        }


# class ReviewForm(forms.ModelForm):

#     class Meta:

#         model=Reviews

#         fields=['comment','rating']