# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, logout, login
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Subject, Section, Student, Document, Lesson
from .utils import handle_message

# Create your views here.


@require_GET
def logout_all(request):
    logout(request)
    request.session.flush()
    return redirect('/')


@require_GET
def index(request):
    context = dict()
    context['message'] = handle_message(request)
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

    request.session['error'] = "نام کاربری یا رمز عبور اشتباه است"
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
    context = {'error': 'نام کاربری یا رمز عبور اشتباه است'}
    return render(request, "admins.html", context)


@require_GET
@login_required(login_url="/")
def admins_panel(request):
    context = dict()
    context['message'] = handle_message(request)
    return render(request, "admin-panel.html", context)


@login_required(login_url="/")
@require_GET
def admins_student_management_section(request):
    context = dict()
    context['message'] = handle_message(request)
    context['section'] = Section.objects.all()
    context['subject'] = Subject.objects.all()
    return render(request, "st-mg.html", context)


@login_required(login_url="/")
@require_POST
def admins_add_student(request):
    if AddStudent(request.POST).is_valid():
        this_college_number = request.POST['college_number']
        this_social_number = request.POST['social_number']
        this_period = request.POST['period']
        this_subject = request.POST['subject']
        this_section = request.POST['section']
        this_last_name = request.POST['last_name']
        this_first_name = request.POST['first_name']
        if not Student.objects.filter(college_number__exact=this_college_number).exists():
            Student(
                college_number=this_college_number,
                social_number=this_social_number,
                last_name=this_last_name,
                first_name=this_first_name,
                period=this_period,
                section=get_object_or_404(Section, id=this_section),
                subject=get_object_or_404(Subject, id=this_subject)
            ).save()
            request.session['done'] = "دانشجو با موفقیت اضافه شد :)"
            return redirect("/admins/panel/student/")
        else:
            request.session['error'] = "دانشجویی با این مشخصات وجود ندارد :/"
            return redirect("/admins/panel/student/")
    return redirect("/")


@login_required(login_url="/")
@require_POST
def admins_delete_student(request):
    if DeleteStudent(request.POST).is_valid():
        this_college_number = int(request.POST['college_number'])
        if Student.objects.filter(college_number__exact=this_college_number).exists():
            Student.objects.filter(college_number__exact=this_college_number).delete()
            request.session['done'] = "دانشجو با موفقیت حذف شد :)"
            return redirect("/admins/panel/student/")
        else:
            request.session['error'] = "دانشجویی با این مشخصات وجود ندارد :/"
            return redirect("/admins/panel/student/")
    else:
        return redirect("/")


@login_required(login_url="/")
@require_POST
def admins_edit_student(request):
    if EditStudent(request.POST).is_valid():
        old_college_number = int(request.POST['old_college_number'])
        this_college_number = int(request.POST['college_number'])
        this_social_number = int(request.POST['social_number'])
        this_last_name = request.POST['last_name']
        this_first_name = request.POST['first_name']
        this_period = request.POST['period']
        this_subject = request.POST['subject']
        this_section = request.POST['section']
        if Student.objects.filter(college_number__exact=old_college_number).exists():
            Student.objects.filter(college_number__exact=old_college_number).update(
                college_number=this_college_number,
                first_name=this_first_name,
                last_name=this_last_name,
                period=this_period,
                social_number=this_social_number,
                subject=get_object_or_404(Subject, id=this_subject),
                section=get_object_or_404(Section, id=this_section)
            )
            request.session['done'] = "دانشجو با موفقیت به‌روز شد :)"
            return redirect("/admins/panel/student/")
        else:
            request.session['error'] = "دانشجویی با این مشخصات وجود ندارد :/"
            return redirect("/admins/panel/student/")
    else:
        return redirect("/")


