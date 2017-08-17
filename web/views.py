# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, logout, login
from django.http.response import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User

from .forms import *
from .models import Subject, Section, Student, PrimaryDocument, Document
from .utils import handle_message

import csv
import os


# Public Views

@require_GET
def media(request):
    if (not request.user.is_anonymous()) or \
            ('student_college_number' in request.session and request.session['student_college_number']) and \
            'image' in request.GET:

        image_file = request.GET['image'].split('/')[3].encode('utf-8')

        if 'student_college_number' in request.session and request.session['student_college_number']:
            path = settings.BASE_DIR + "/docs/" + str(request.session['student_college_number']) + "/"
        elif not request.user.is_anonymous():
            path = settings.BASE_DIR + "/docs/" + str(request.GET['student']) + "/"
        else:
            return redirect("/")

        try:
            with open(os.path.join(path, image_file.decode('utf-8')), str("rb")) as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except IOError:
            return HttpResponseNotFound()

    else:
        return redirect("/")


@require_GET
def logout_all(request):
    logout(request)
    request.session.flush()
    return redirect('/')


@require_POST
def upload_document(request):
    if (not request.user.is_anonymous()) or \
            ('student_college_number' in request.session and request.session['student_college_number']):
        form = DocumentUpload(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image'].size > 262144:
                request.session['error'] = 'سایز فایل از ۲۵۰ کیلو بایت بیشتر است :/'
                return redirect("/")
            is_primary = False
            image_type = form.cleaned_data['type']
            this_student = request.POST['student']
            if PrimaryDocument.objects.filter(name__exact=image_type).exists():
                is_primary = True

            Document(
                student=get_object_or_404(Student, college_number=this_student),
                type=image_type,
                primary=is_primary,
                doc=form.cleaned_data['image']
            ).save()

            request.session['done'] = 'مدرک با موفقیت آپلود شد :)'

            if 'student_college_number' in request.session and request.session['student_college_number']:
                return redirect("/")
            elif not request.user.is_anonymous():
                return redirect("/admins/panel/student/view?search="+request.POST['student'])
        else:
            request.session['error'] = 'فایل فرستاده شده اشتباه می‌باشد :/'
            return redirect("/")
    else:
        return redirect("/")


@require_GET
def index(request):
    context = dict()
    context['message'] = handle_message(request)
    if 'student_college_number' in request.session and request.session['student_college_number']:
        this_student = get_object_or_404(Student, college_number=request.session['student_college_number'])
        context['docs'] = Document.objects.filter(student=this_student)
        context['primary_docs'] = PrimaryDocument.objects.all()
        return render(request, "st-panel.html", context)
    return render(request, "index.html", context)


# Student Actions

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


# Admins Actions

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


@login_required(login_url="/")
@require_POST
def admins_upload_student(request):
    if 'students_info' in request.FILES:
        this_student_info = request.FILES['students_info']
        if this_student_info.content_type == 'text/csv':
            reader = csv.reader(this_student_info, delimiter=str(u","))
            this_period = this_section = this_last_name = this_first_name = this_college_number = \
                this_social_number = this_subject = ''
            row = list(reader)
            for i in range(0, len(row[0])):
                if row[0][i] == 'section':
                    this_section = i
                elif row[0][i] == 'last_name':
                    this_last_name = i
                elif row[0][i] == 'first_name':
                    this_first_name = i
                elif row[0][i] == 'college_number':
                    this_college_number = i
                elif row[0][i] == 'social_number':
                    this_social_number = i
                elif row[0][i] == 'period':
                    this_period = i
                elif row[0][i] == 'subject':
                    this_subject = i
                else:
                    request.session['error'] = 'لطفا همانند الگو فایل را قالب بندی کنید :('
                    return redirect("/admins/panel/student/")
            for r in row:
                if r[this_college_number] == "college_number":
                    continue

                print r[this_section]
                if r[this_section].decode('utf8') == "کاردانی پیوسته":
                    this_section_value = get_object_or_404(Section, name="کاردانی")
                elif r[this_section].decode('utf8') == "کارشناسی ناپیوسته":
                    this_section_value = get_object_or_404(Section, name="کارشناسی")

                if not Subject.objects.filter(name=r[this_subject].decode('utf8')).exists():
                    Subject(
                        name=r[this_subject].decode('utf8'),
                        section=this_section_value
                    ).save()

                if Student.objects.filter(college_number__exact=r[this_college_number]).exists():
                    continue

                this_row = Student(
                    college_number=r[this_college_number],
                    social_number=r[this_social_number],
                    first_name=r[this_first_name].decode('utf8'),
                    last_name=r[this_last_name].decode('utf8'),
                    subject=get_object_or_404(Subject, name=r[this_subject].decode('utf8')),
                    section=this_section_value,
                    period=r[this_period].decode('utf8'),
                )
                this_row.save()
            request.session['done'] = 'اطلاعات با موفقیت به ثبت رسید :)'
            return redirect("/admins/panel/student/")
        else:
            request.session['error'] = 'فایل باید با فرمت csv آپلود شود :/'
            return redirect("/admins/panel/student/")
    request.session['error'] = 'فایل فرستاده شده ناقص می‌باشد :/'
    return redirect("/admins/panel/student/")


@require_GET
@login_required(login_url="/")
def admins_view_new_docs(request):
    context = dict()
    context['message'] = handle_message(request)
    return render(request, "view.html", context)


@require_GET
@login_required(login_url="/")
def admins_staff_management(request):
    context = dict()
    context['message'] = handle_message(request)
    return render(request, "view-staff.html", context)


@require_GET
@login_required(login_url="/")
def admins_view_students(request):
    if 'search' in request.GET:
        context = dict()
        this_search_key = int(request.GET['search'])
        context['message'] = handle_message(request)
        context['docs'] = Document.objects.filter(student__college_number__exact=this_search_key)
        context['student_info'] = Student.objects.get(college_number__exact=this_search_key)
        context['primary_docs'] = PrimaryDocument.objects.all()
        return render(request, "search-result.html", context)
    request.session['error'] = 'خطا :('
    return redirect("/admins/panel/")


@require_GET
@login_required(login_url="/")
def admins_setting(request):
    context = dict()
    context['message'] = handle_message(request)
    return render(request, "admin-setting.html", context)


@require_POST
@login_required(login_url="/")
def admins_password_change(request):
    if PasswordChange(request.POST).is_valid():
        new_pass = request.POST['new_password']
        repeat_pass = request.POST['repeat_password']
        old_pass = request.POST['old_password']

        if not new_pass == repeat_pass:
            request.session['error'] = 'دو رمز عبور وارد شده با هم برابر نمی‌باشد :('
            return redirect("/admins/panel/setting/")
        elif old_pass == new_pass:
            request.session['error'] = 'رمز عبور فعلی با رمز عبور جدید برابر است :/'
            return redirect("/admins/panel/setting/")

        this_user = User.objects.get(username__exact=request.user.username)

        if not this_user.check_password(old_pass):
            request.session['error'] = 'رمز عبور فعلی معتبر نمی‌باشد :('
            return redirect("/admins/panel/setting/")

        this_user.set_password(new_pass)
        this_user.save()

        request.session['done'] = 'رمز عبور شما با موفقیت تغییر کرد :)'
        return redirect("/admins/panel/setting/")

    request.session['error'] = 'خطا :('
    return redirect("/admins/panel/setting/")


@require_POST
@login_required(login_url="/")
def add_main_doc(request):
    if PrimaryDocumentName(request.POST).is_valid():
        this_main_doc = request.POST['name']
        if PrimaryDocument.objects.filter(name__exact=this_main_doc).exists():
            request.session['error'] = 'این مورد موجود می‌باشد :('
            return redirect("/admins/panel/setting/")
        PrimaryDocument(
            name=this_main_doc
        ).save()
        request.session['done'] = 'نام مدرک اصلی با موفقیت اضافه شد :)'
        return redirect("/admins/panel/setting/")
    request.session['error'] = 'خطا :('
    return redirect("/admins/panel/setting/")


@require_POST
@login_required(login_url="/")
def accept_reject_docs(request):
    if 'doc' in request.POST:
        this_doc_id = request.POST['doc']
        this_document = Document.objects.get(id=this_doc_id)
        if this_document:
            is_accepted = False if this_document.is_accepted else True
            this_document.update(
                is_accepted=is_accepted
            )
            request.session['done'] = 'وضعیت مدرک با موفقیت تغییر کرد :)'
            return redirect("/admins/panel/setting/")
    request.session['error'] = 'خطا :('
    return redirect("/admins/panel/setting/")

