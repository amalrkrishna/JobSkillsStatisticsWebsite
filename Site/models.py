# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.conf import settings
import datetime


class JobSkill(models.Model):
    name = models.CharField(max_length=64, unique=True)
    skills = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    title = models.CharField(max_length=64)
    company = models.CharField(blank=True, max_length=64)
    description = models.TextField(blank=True, max_length=10000)
    city = models.CharField(blank=True, max_length=64)
    state = models.CharField(blank=True, max_length=2)  # convert to abbreviation
    date_posted = models.DateTimeField(null=True, blank=True, auto_now=False)
    date_entered = models.DateTimeField(auto_now=True)
    is_sponsored = models.BooleanField(verbose_name="Sponsored")
    category = models.ForeignKey(JobSkill, null=True, blank=True, on_delete=models.CASCADE)
    skills = models.CharField(blank=True, max_length=500)


class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company')
