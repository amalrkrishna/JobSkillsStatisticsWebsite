# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from Site.models import *


admin.site.register(JobPosting, JobPostingAdmin)
admin.site.register(JobSkill)
