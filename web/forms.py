from django import forms


class StudentLogin(forms.Form):
    username = forms.IntegerField(label='username')
    password = forms.IntegerField(label='password')


class AdminLogin(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')
