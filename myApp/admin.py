# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from myApp.models import *


admin.site.register(JobPosting, JobPostingAdmin)
