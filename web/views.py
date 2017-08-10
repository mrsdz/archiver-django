# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, logout, login
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .forms import *
from .models import Subject, Section, Student, Document, Lesson
from .utils import handle_error_message

# Create your views here.


@require_GET
def logout_all(request):
    logout(request)
    request.session.flush()
    return redirect('/')


@require_GET
def index(request):
    context = handle_error_message(request)
    if 'student_college_number' in request.session and request.session['student_college_number']:
        return render(request, "st-panel.html", context)
    return render(request, "index.html", context)


@require_POST
def student_login(request):
    if StudentLogin(request.POST).is_valid():
        this_username = int(request.POST['username'])
        this_password = int(request.POST['password'])
        if Student.objects.filter(college_number=this_username).exists():
            this_student = Student.objects.get(college_number=this_username)
            if this_password == int(this_student.social_number):
                request.session['student_first_name'] = this_student.first_name
                request.session['student_last_name'] = this_student.last_name
                request.session['student_college_number'] = this_student.college_number
                request.session['student_subject'] = this_student.subject.name
                request.session['student_period'] = this_student.period
                request.session['student_section'] = this_student.section.name
                return redirect('/', request)

    request.session['error'] = {'error': 'forbidden'}
    return redirect('/')


@require_POST
def admin_login(request):
    if AdminLogin(request.POST).is_valid():
        this_username = request.POST['username']
        this_password = request.POST['password']
        this_user = authenticate(username=this_username, password=this_password)
        if this_user is not None:
            if this_user.is_active:
                login(request, this_user)
                return redirect('/admins/panel/')
            else:
                HttpResponse("Your Account is disable.")
    context = {'error': 'Forbidden'}
    return render_to_response("admins.html", context)


@require_GET
@login_required(login_url="/")
def admins_panel(request):
    return render_to_response("ad-panel.html")


@login_required(login_url="/")
@require_POST
def admins_add_student(request):
    if AddStudent(require_POST).is_valid():
        this_college_number = request.POST['college_number']
        this_social_number = request.POST['social_number']
        this_period = request.POST['period']
        this_subject = request.POST['subject']
        this_section = request.POST['section']
        this_last_name = request.POST['last_name']
        this_first_name = request.POST['first_name']
        try:
            Student(
                college_number=this_college_number,
                social_number=this_social_number,
                last_name=this_last_name,
                first_name=this_first_name,
                period=this_period,
                section=get_object_or_404(Section, id=this_section),
                subject=get_object_or_404(Subject, id=this_subject)
            ).save()
        except IntegrityError:
            request.session['error'] = "دانشجویی با این مشخصات وجود دارد :/"
            return redirect("admins/panel/student/")

        request.session['done'] = "دانشجو با موفقیت اضافه شد :)"
        return redirect("admins/panel/student/")


