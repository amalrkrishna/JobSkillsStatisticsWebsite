# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from Site.forms import *
from Site.models import *
from Scraper import DisplayData
from django.views.generic import TemplateView
import datetime
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



def glassdoor_database(request):
    data = pd.read_excel('data/LPR_data-2018-01.xlsx')
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    return render(request, 'glassdoor_database.html', context)

def indeed_database(request):
    job_postings = JobPosting.objects.all()  # order by date
    return render(request, 'indeed_database.html', {'job_postings': job_postings})

def database(request):
    return render(request, 'database.html')

def landing_page(request):
    return render(request, 'landing.html')

def indeed(request):
    return render(request, 'indeed.html')

class Plot(TemplateView):
    template_name = "plot.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot, self).get_context_data(**kwargs)
        context['plot'] = DisplayData.GetSkillsFromJobRegion("data analyst", "Boston, MA")
        return context

class PlotGlassDoor(TemplateView):
    template_name = "glassdoor.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotGlassDoor, self).get_context_data(**kwargs)
        context['plot1'] = DisplayData.GlassdoorPlot1()
        context['plot2'] = DisplayData.GlassdoorPlot2()
        context['plot3'] = DisplayData.GlassdoorPlot3()
        context['plot4'] = DisplayData.GlassdoorPlot4()
        context['plot5'] = DisplayData.GlassdoorPlot5()

        return context

@csrf_exempt
def indeed_form_submit(request):
    if request.method == "POST":
        city = request.POST.get('sel1')
        job_title = request.POST.get('sel2')
        print(job_title,city)
        plot = DisplayData.GetSkillsFromJobRegion(job_title,city)
        return render(request, 'indeed.html', plot)
