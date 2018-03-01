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
from django.template.loader import render_to_string
import plotly.plotly as py
import plotly.graph_objs as go



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


class IndeedPlot(TemplateView):
    template_name = "indeed.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndeedPlot, self).get_context_data(**kwargs)
        context['plot'] = DisplayData.GetSkillsFromJobRegion(kwargs['job'], kwargs['city'])
        return context

@csrf_exempt
def indeed(request):
    if request.method == 'GET' and 'job' in request.GET:
        job=request.GET['job']
        city=request.GET['city']
        g = IndeedPlot()
        context = g.get_context_data(job=job, city=city)
        return render(request, 'indeed.html', context)
    else:
        return render(request, 'indeed.html')

class Plot(TemplateView):
    template_name = "plot.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot, self).get_context_data(**kwargs)
        context['plot'] = DisplayData.GetSkillsFromJobRegion("data analyst", "Boston, MA")
        print(context['plot'])
        return context

class PlotGlassDoor(TemplateView):
    template_name = "glassdoor.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotGlassDoor, self).get_context_data(**kwargs)
        context['plot'] = DisplayData.GlassdoorPlot1(kwargs['genstat'])
        return context

class PlotGlassDoorBox(TemplateView):
    template_name = "glassdoor.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotGlassDoorBox, self).get_context_data(**kwargs)
        context['plot6'] = DisplayData.GlassdoorPlot6(kwargs['boxplot'])
        return context

class PlotGlassDoorBox2(TemplateView):
    template_name = "glassdoor.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotGlassDoorBox2, self).get_context_data(**kwargs)
        context['plot2'] = DisplayData.GlassdoorPlot2(kwargs['boxplot'])
        return context

@csrf_exempt
def glassdoor(request):
    if request.method == 'GET' and 'genstat' in request.GET:
        genstat=request.GET['genstat']
        g = PlotGlassDoor()
        context = g.get_context_data(genstat=genstat)
        return render(request, 'glassdoor.html', context)
    elif request.method == 'GET' and 'boxplot' in request.GET:
        boxplot=request.GET['boxplot']
        if boxplot == 'Median Base Pay':
            g = PlotGlassDoorBox()
            context = g.get_context_data(boxplot=boxplot)
            return render(request, 'glassdoor.html', context)
        else:
            g = PlotGlassDoorBox2()
            context = g.get_context_data(boxplot=boxplot)
            return render(request, 'glassdoor.html', context)
    else:
        return render(request, 'glassdoor.html')