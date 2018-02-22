# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from Site.forms import *
from Site.models import *
from Scraper import DisplayData
from django.views.generic import TemplateView
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

class Plot(TemplateView):
    template_name = "plot.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot, self).get_context_data(**kwargs)
        context['plot'] = DisplayData.GetSkillsFromJobRegion("data analyst", "Boston, MA")
        return context
