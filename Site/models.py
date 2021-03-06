# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.conf import settings
import datetime

JOB_CATEGORIES = (
    ('data_scientist', 'Data Scientist'),
    ('test', 'Test')
)

class JobSkill(models.Model):
    category = models.CharField(max_length=64, choices=JOB_CATEGORIES)
    skill = models.CharField(max_length=64)

    def __str__(self):
        return self.skill


class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'category')

class GlassDoorModel(models.Model):
    metro = models.CharField(max_length=64)
    dimension_type = models.CharField(blank=True, max_length=64, default='')
    month  = models.DateTimeField(null=True, blank=True, auto_now=False)
    dimension = models.CharField(blank=True, max_length=64, default='')
    measure = models.CharField(blank=True, max_length=64, default='')
    value = models.CharField(blank=True, max_length=64, default='')
    yoy = models.CharField(blank=True, max_length=64, default='')

class JobPosting(models.Model):
    # job_id = models.CharField(max_length=16, unique=True)  # default=None
    title = models.CharField(max_length=64)
    company = models.CharField(blank=True, max_length=64, default='')
    description = models.TextField(blank=True, max_length=10000, default='')
    city = models.CharField(blank=True, max_length=64, default='')
    state = models.CharField(blank=True, max_length=2, default='', help_text='State abbreviations only.')
    date_posted = models.DateTimeField(null=True, blank=True, auto_now=False)
    date_entered = models.DateTimeField(auto_now=True)
    is_sponsored = models.BooleanField(verbose_name="Sponsored")
    skills = models.ManyToManyField(JobSkill, blank=True, default='')

    def save(self):
        # change full name state to its abbreviation
        state_abbreviation_list = [
            ('Alabama', 'AL'),
            ('Alaska', 'AK'),
            ('Arizona', 'AZ'),
            ('Arkansas', 'AR'),
            ('California', 'CA'),
            ('Colorado', 'CO'),
            ('Connecticut', 'CT'),
            ('Delaware', 'DE'),
            ('Florida', 'FL'),
            ('Georgia', 'GA'),
            ('Hawaii', 'HI'),
            ('Idaho', 'ID'),
            ('Illinois', 'IL'),
            ('Indiana', 'IN'),
            ('Iowa', 'IA'),
            ('Kansas', 'KS'),
            ('Kentucky', 'KY'),
            ('Louisiana', 'LA'),
            ('Maine', 'ME'),
            ('Maryland', 'MD'),
            ('Massachusetts', 'MA'),
            ('Michigan', 'MI'),
            ('Minnesota', 'MN'),
            ('Mississippi', 'MS'),
            ('Missouri', 'MO'),
            ('Montana', 'MT'),
            ('Nebraska', 'NE'),
            ('Nevada', 'NV'),
            ('New Hampshire', 'NH'),
            ('New Jersey', 'NJ'),
            ('New Mexico', 'NM'),
            ('New York', 'NY'),
            ('North Carolina', 'NC'),
            ('North Dakota', 'ND'),
            ('Ohio', 'OH'),
            ('Oklahoma', 'OK'),
            ('Oregon', 'OR'),
            ('Pennsylvania', 'PA'),
            ('Rhode Island', 'RI'),
            ('South Carolina', 'SC'),
            ('South Dakota', 'SD'),
            ('Tennessee', 'TN'),
            ('Texas', 'TX'),
            ('Utah', 'UT'),
            ('Vermont', 'VT'),
            ('Virginia', 'VA'),
            ('Washington', 'WA'),
            ('West Virginia', 'WV'),
            ('Wisconsin', 'WI'),
            ('Wyoming', 'WY'),
            ('Guam', 'GU'),
            ('Puerto Rico', 'PR'),
            ('Virgin Islands', 'VI'),
            ('District of Columbia', 'DC'),
            ('American Samoa', 'AS'),
            ('Federated States of Micronesia', 'FM'),
            ('Marshall Islands', 'MH'),
            ('Northern Mariana Islands', 'MP'),
            ('Palau', 'PW')
        ]
        found = False
        if len(self.state) > 2:
            for full_name, abbreviation in state_abbreviation_list:
                if self.state.lower() == full_name.lower():
                    self.state = abbreviation
                    found = True
        if not len(self.state) == 2 and not found:
            self.state = ''  # changes to empty string if invalid state
        self.state.upper()
        super(JobPosting, self).save()

class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'city', 'state', 'date_posted')
    
class Geography(models.Model):
    Country =       models.CharField(max_length = 64, default = '')
    CountryCode =   models.IntegerField(default = -1)
    Area =          models.CharField(max_length = 64, default = '')
    AreaCode =      models.IntegerField(default = -1)
    SubArea =       models.CharField(max_length = 64, default = '')
    SubAreaCode =   models.IntegerField(default = -1)
    
class JobSkillCount(models.Model):
    job_skill = models.ForeignKey(
        'JobSkill',
        on_delete = models.CASCADE,
        default = None)
    posted_count =  models.IntegerField(default=0)
   
class Cities(models.Model):
    Country =       models.CharField(max_length = 64, default = '')
    CountryCode =   models.IntegerField(default = -1)
    Area =          models.CharField(max_length = 64, default = '')
    AreaCode =      models.IntegerField(default = -1)
    County = 		models.CharField(max_length = 64, default = '')
    CountyCode = 	models.IntegerField(default = -1)
    City =          models.CharField(max_length = 64, default = '')

class Jobs(models.Model):
    category = models.CharField(max_length=64, choices=JOB_CATEGORIES)
    
class Skills(models.Model):
    skill = models.CharField(max_length=64)

class JobSkillRegionDateCount(models.Model):
    job = models.ForeignKey(
        'Jobs',
        on_delete = models.CASCADE,
        default = None)
    skill = models.ForeignKey(
        'Skills',
        on_delete = models.CASCADE,
        default = None)
    geography =     models.ForeignKey(
        'Geography',
        on_delete = models.CASCADE,
        default = None)
    start_date =    models.DateTimeField(null = True, blank = True, auto_now = False)
    end_date =      models.DateTimeField(null = True, blank = True, auto_now = False)
    posted_count =  models.IntegerField(default = 0)
    
class JobSkillCityDateCount(models.Model):
    job = models.ForeignKey(
        'Jobs',
        on_delete = models.CASCADE,
        default = None)
    skill = models.ForeignKey(
        'Skills',
        on_delete = models.CASCADE,
        default = None)
    city =     models.ForeignKey(
        'Cities',
        on_delete = models.CASCADE,
        default = None)
    start_date =    models.DateTimeField(null = True, blank = True, auto_now = False)
    end_date =      models.DateTimeField(null = True, blank = True, auto_now = False)
    posted_count =  models.IntegerField(default = 0)