from django import forms
from django.contrib.auth.models import User
from .models import File


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    firstname = forms.CharField(widget=forms.TextInput)
    lastname = forms.CharField(widget=forms.TextInput)
    class Meta():
        model = User
        fields = ('firstname', 'lastname', 'username','password','email')

class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["xls", "csv", "xlsx"]:
            raise forms.ValidationError("Only xls, csv and xlsx files are allowed.")
        # return cleaned data is very important.
        return file