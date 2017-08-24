# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Subject, Section, Student, Document, PrimaryDocument, UsersJob

# Register your models here.

admin.site.register(Student)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Document)
admin.site.register(PrimaryDocument)
admin.site.register(UsersJob)

