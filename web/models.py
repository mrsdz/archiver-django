# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "{}-{}".format(self.name, self.id)


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

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


class Lesson(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject)
    section = models.ForeignKey(Section)
    lesson_type = models.CharField(max_length=120, default=0)
    unit = models.IntegerField(default=1)

    def __unicode__(self):
        return "{}".format(self.code)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    # TODO: Must pass a function upload_to :)
    doc = models.ImageField()

    def __unicode__(self):
        return "{}-{}-{}".format(self.id, self.student.college_number, self.type)



