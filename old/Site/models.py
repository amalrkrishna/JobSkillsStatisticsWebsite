# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.conf import settings
import datetime


class JobPosting(models.Model):
    title = models.CharField(max_length=64, default='Unknown Job Title')
    company = models.CharField(null=True, blank=True, max_length=64)
    description = models.TextField(null=True, blank=True, max_length=5000)
    # TODO
    # city
    # state
    # date posted
    # date entered
    # sponsored


class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company')


# TODO job title and and skill list table
# TODO job ID and skill entry table
