# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.conf import settings
import datetime
# from django_mysql.models import ListCharField


class JobPosting(models.Model):
    title = models.CharField(max_length=64)
    company = models.CharField(blank=True, max_length=64)
    description = models.TextField(blank=True, max_length=10000)
    # city
    # state
    # date posted
    # date entered
    # sponsored
    # skills


class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company')


class JobSkill(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # skills = ListCharField(blank=True, max_length=64)


class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('name', )
