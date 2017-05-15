from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.base_user import AbstractBaseUser
from datetime import datetime
from django.contrib.auth.models import UserManager
import os


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Student(AbstractBaseUser):
    sid = models.CharField(max_length=9, blank=False, null=False, unique=True)
    # salt = ... (are these necessary?)
    # hash = ... (are these necessary?)
    name = models.CharField(max_length=70, blank=False, null=False)
    bio = models.CharField(max_length=500, blank=True, null=True)
    # Not sure if/how this will work -- got any better ideas?
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    student_years = (('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'),
            ('Junior', 'Junior'), ('Senior', 'Senior'),
            ('1st Year Graduate', '1st Year Graduate'),
            ('2nd Year Graduate', '2nd Year Graduate'),
            ('1st Year PhD', '1st Year PhD'), ('2nd Year PhD', '2nd Year PhD'),
            ('3rd Year PhD', '3rd Year PhD'), ('4th Year PhD', '4th Year PhD'))
    student_year = models.CharField(max_length=17, choices=student_years, blank=False, null=False)
    days_joined = models.IntegerField(blank=True, null=True, default=0)
    days_active = models.IntegerField(blank=True, null=True, default=0)

    objects = UserManager()

    USERNAME_FIELD = 'sid'

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.sid

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True,
            blank=True, default=-1)
    years_exp_total = models.IntegerField(blank=True, null=True, default=0)
    years_exp_sjsu = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


class ActiveCourse(models.Model):
    cid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10, blank=False, null=False)
    section = models.IntegerField(blank=False, null=False)
    terms = (('Fall', 'Fall'), ('Winter', 'Winter'), ('Spring', 'Spring'),
            ('Summer', 'Summer'))
    term = models.CharField(max_length=6, choices=terms, blank=False, null=False)
    year = models.IntegerField(default=datetime.now().year, blank=False, null=False,
            validators=[MinValueValidator(2000),
                MaxValueValidator(datetime.now().year + 1)])
    instructor = models.ForeignKey(Instructor, blank=False, null=False)

    def __str__(self):
        return self.name + " " + str(self.cid)


class Review(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False)
    course = models.ForeignKey(Course, blank=False, null=False)
    instructor = models.ForeignKey(Instructor, blank=False, null=False)
    title = models.CharField(max_length=70, blank=False, null=False)
    body = models.CharField(max_length=500, blank=False, null=False)
    rating = models.DecimalField(max_digits=2, decimal_places= 1, blank=False,
            null=False)


class PastCourse(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False)
    course = models.ForeignKey(Course, blank=False, null=False)
    instructor = models.ForeignKey(Instructor, blank=False, null=False)


class CurrentCourse(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False)
    course = models.ForeignKey(ActiveCourse, blank=False, null=False)


class FutureCourse(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False)
    course = models.ForeignKey(Course, blank=False, null=False)


class Friend(models.Model):
    user = models.ForeignKey(Student, blank=False, null=False,
            related_name='friendA')
    friend = models.ForeignKey(Student, blank=False, null=False,
            related_name='friendB')
