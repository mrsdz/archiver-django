# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from .models import UsersJob


def handle_message(request):
    if "error" in request.session:
        context = {'error': request.session['error']}
        del request.session['error']
        return context
    elif "done" in request.session:
        context = {'done': request.session['done']}
        del request.session['done']
        return context
    return


def perm(request):
    this_user = get_object_or_404(User, username=request.user.get_username())
    this_user_job = UsersJob.objects.filter(user=this_user)
    request.session['job'] = this_user_job[0].job
    return


def has_perm_admin(request):
    return True if request.session['job'] == 'A' else False


def has_perm_admin_or_archive(request):
    return True if request.session['job'] == 'A' or request.session['job'] == 'B' else False
