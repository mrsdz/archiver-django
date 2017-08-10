from django import forms


class StudentLogin(forms.Form):
    username = forms.IntegerField(label='username')
    password = forms.IntegerField(label='password')


class AdminLogin(forms.Form):
    username = forms.CharField(label='username', max_length=30)
    password = forms.CharField(label='password', max_length=30)


class AddStudent(forms.Form):
    last_name = forms.CharField(label='last_name', max_length=200)
    first_name = forms.CharField(label='first_name', max_length=200)
    social_number = forms.IntegerField(label='social_number')
    college_number = forms.IntegerField(label='college_number')
    subject = forms.CharField(label='subject', max_length=200)
    section = forms.CharField(label='section', max_length=200)
    period = forms.CharField(label='period', max_length=200)


class DeleteStudent(forms.Form):
    college_number = forms.IntegerField(label='college_number')


class EditStudent(forms.Form):
    old_college_number = forms.IntegerField(label='old_college_number')
    last_name = forms.CharField(label='last_name', max_length=200)
    first_name = forms.CharField(label='first_name', max_length=200)
    social_number = forms.IntegerField(label='social_number')
    college_number = forms.IntegerField(label='college_number')
    subject = forms.CharField(label='subject', max_length=200)
    section = forms.CharField(label='section', max_length=200)
    period = forms.CharField(label='period', max_length=200)


class AddStaffer(forms.Form):
    last_name = forms.CharField(label='last_name', max_length=200)
    first_name = forms.CharField(label='first_name', max_length=200)
    password = forms.CharField(label='password')
    email = forms.EmailField(label='email')
    username = forms.CharField(label='username', max_length=200)


class DeleteStaffer(forms.Form):
    username = forms.CharField(label='username', max_length=200)

