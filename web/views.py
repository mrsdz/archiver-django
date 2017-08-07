# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from .forms import *
from .models import *


# Create your views here.

def logout(request):
    request.session.flush()
    return redirect('/')


def index(request):
    context = dict()
    if "error" in request.session:
        del request.session['error']
        context = {'error': 'forbidden'}
    elif 'student_college_number' in request.session and request.session['student_college_number']:
        return render(request, "st-panel.html", context)
    return render(request, "index.html", context)


@require_POST
def student_login(request):
    if StudentLogin(request.POST).is_valid():
        this_username = request.POST['username']
        this_password = request.POST['password']
        if Student.objects.filter(college_number=this_username).exists():
            this_student = Student.objects.get(college_number=this_username)
            if int(this_password) == int(this_student.social_number):
                request.session['student_first_name'] = this_student.first_name
                request.session['student_last_name'] = this_student.last_name
                request.session['student_college_number'] = this_student.college_number
                request.session['student_subject'] = this_student.subject.name
                request.session['student_period'] = this_student.period
                request.session['student_section'] = this_student.section.name
                return redirect('/', request)

    request.session['error'] = {'error': 'forbidden'}
    return redirect('/')
