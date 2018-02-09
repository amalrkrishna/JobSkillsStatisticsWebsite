# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render


def home(request):
    job_postings = JobPosting.objects.all()  # order by date

    return render(request, 'home.html', {'job_postings': job_postings})
