# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from Site.forms import *
from Site.models import *
import datetime


def home(request):
    job_postings = JobPosting.objects.all()  # order by date

    return render(request, 'home.html', {'job_postings': job_postings})

def landing_page(request):
    return render(request, 'landing.html')

