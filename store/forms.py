from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from store.models import UserProfile,Project

class SignUpForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}))


    class Meta:

        model=User

        fields=["username","email","password1","password2"]

        widgets={

            "username":forms.TextInput(attrs={"class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}),
            "email":forms.EmailInput(attrs={"class":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}),
        }



class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"w-full flex-1 appearance-none border-gray-300 bg-white px-4 py-2 text-base text-gray-700 placeholder-gray-400 focus:outline-none","placeholder":"Enter Your Username"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"w-full flex-1 appearance-none border-gray-300 bg-white px-4 py-2 text-base text-gray-700 placeholder-gray-400 focus:outline-none","placeholder":"Enter Your Password"}))        



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