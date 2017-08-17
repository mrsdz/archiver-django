# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible


def path_rename(instance, filename):
    name = get_random_string(length=24) + "." + filename.split('.')[-1]
    path = "docs/" + str(instance.student_id) + "/"
    full = path + name
    return full


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "{}-{}".format(self.name, self.id)


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    section = models.ForeignKey(Section)

    def __unicode__(self):
        return "{}-{}".format(self.id, self.name)


class Student(models.Model):
    college_number = models.BigIntegerField(primary_key=True)
    social_number = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    section = models.ForeignKey(Section)
    period = models.CharField(max_length=120)
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return "{}".format(self.college_number)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    primary = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    doc = models.ImageField(upload_to=path_rename)
    is_accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return "{}-{}-{}".format(self.id, self.student.college_number, self.type)


class PrimaryDocument(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "{}-{}".format(self.id, self.name)
