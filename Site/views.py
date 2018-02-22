# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from Site.forms import *
from Site.models import *
import datetime


def database(request):
    job_postings = JobPosting.objects.all()  # order by date

    return render(request, 'database.html', {'job_postings': job_postings})

def landing_page(request):
    data = "hello"
    return render(request, 'landing.html', {'data':data})

def indeed(request):
    return render(request, 'indeed.html')

def glassdoor(request):
    return render(request, 'glassdoor.html')

