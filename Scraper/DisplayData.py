import pandas as pd
import django
django.setup()
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from Site.models import *
from Scraper import preprocessing
from Scraper import scraper
from Scraper import DisplayData
import os
from django.db.models import Q

def GetSkillsFromJobRegionDateCount(job, region):
    job_rows = Jobs.objects.filter(category =job).all()
    category = job_rows[0].category
    job_id = job_rows[0].id
    
    region_array = region.split(", ")
    city_row = Cities.objects.filter(City = region_array[0], Area = region_array[1]).all()
    city_id = city_row[0].id
    
    skills = Skills.objects.all()
    
    
    job_skill_return = []
    for skill_row in skills:
        
        skill = skill_row.skill
        skill_id = skill_row.id
        print(skill)
        try:
            job_skill_count = JobSkillCityDateCount.objects.get(job_id = job_id, skill_id = skill_id, city_id = city_id)
            job_skill_return.append((skill, job_skill_count.posted_count))
        except:
            job_skill_return.append((skill, 0))
        
    df = pd.DataFrame( [[ij for ij in i] for i in job_skill_return] )
    print(df[1])
    graphData = go.Bar(
        x=df[0],
        y=df[1])
    
    graphLayout = go.Layout(
        title='Skills vs Count',
        showlegend=False,
        autosize=False,
        width=1100,
        height=800,
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
            title='Count'
        )
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_div = plot(figure, output_type='div', include_plotlyjs=False)
    '''return url'''
    return plot_div


def GetSkillsFromJobRegion(job, region):
    job_skills = JobSkill.objects.filter(category = job).all()
    
    job_skill_return = []
    for job_skill in job_skills:
        skill = job_skill.skill
        print(skill)
        try:
            print("try")
            job_skill_count = 2
            job_skill_other_count = JobSkillRegionDateCount.objects.get(job_skill_id = 114, geography_id = 1218)
            print("2")
            print(job_skill_other_count.posted_count)
            '''#JobSkillRegionDateCount.objects.get(job_skill_id = 114, geography_id = 1218)'''
            print("Count")
            print(str(job_skill_count))
            job_skill_return.append((skill, job_skill_count))
        except:
            job_skill_return.append((skill, 0))
            print("Except")
        
    df = pd.DataFrame( [[ij for ij in i] for i in job_skill_return] )
    print(df[1])
    graphData = go.Bar(
        x=df[0],
        y=df[1])
    
    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        title='Skills vs Count',
        showlegend=False,
        autosize=False,
        width=1100,
        height=800,
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
            title='Count'
        )
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_div = plot(figure, output_type='div', include_plotlyjs=False)
    '''return url'''
    return plot_div


def CompareJobsPlot(job1, job2):
    #jobs = pd.DataFrame(list(Jobs.objects.filter(Q(category=job1) | Q(category=job2)).values()))

    job1_skills = pd.DataFrame(list(JobSkillRegionDateCount.objects.filter(job__category=job1).all().values()))
    job2_skills = pd.DataFrame(list(JobSkillRegionDateCount.objects.filter(job__category=job2).all().values()))

    #sum post counts by skill
    job1_skills = job1_skills[['skill_id', 'posted_count']].groupby('skill_id', as_index=False).sum()
    job2_skills = job2_skills[['skill_id', 'posted_count']].groupby('skill_id', as_index=False).sum()

    #add skill names
    skills = pd.DataFrame(list(Skills.objects.all().values()))
    skills = pd.merge(skills, job1_skills, left_on='id', right_on='skill_id')
    skills = pd.merge(skills, job2_skills, left_on='id', right_on='skill_id')
    skills.columns= ['id', 'skill', 'skill_id1', 'job1_count', 'skill_id2', 'job2_count']
    #rank skills by post count
    skills['job1_rank'] = skills['job1_count'].rank(ascending=False)
    skills['job2_rank'] = skills['job2_count'].rank(ascending=False)

    graph = go.Scatter(
        x = skills['job1_rank'],
        y = skills['job2_rank'],
        text = skills['skill'],
        mode='text',
        hoverinfo= 'text+x+y'
    )

    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        title='Skills: ' + job1 + ' vs ' + job2,
        showlegend=False,
        autosize=False,
        width=1100,
        height=800,
        xaxis=dict(
            autorange='reversed',
            title=job1 + ' skill rank',
            zeroline=False
        ),
        yaxis=dict(
            autorange='reversed',
            title= job2 + ' skill rank',
            zeroline=False
        )
    )

    figure = go.Figure(data=[graph], layout=graphLayout)
    plot_div = plot(figure, output_type='div', include_plotlyjs=False)
    '''return url'''
    return plot_div

def GlassdoorPlot1(genstat):
    Jan2018 = pd.read_excel('data/LPR_data-2018-01.xlsx')

    USMetro = Jan2018[Jan2018['Measure'] == genstat]
    print(USMetro)

    graphData = go.Bar(
        x=USMetro['Metro'],
        y=USMetro['Value'])
    
    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        title=genstat+' in top US Cities',
        showlegend=False,
        autosize=False,
        width=1100,
        height=800,
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
            title=genstat
        )
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_USMetro = plot(figure, output_type='div', include_plotlyjs=False)
    print(plot_USMetro)
    return plot_USMetro

def GlassdoorPlot2(boxplot2):
    Jan2018 = pd.read_excel('data/LPR_data-2018-01.xlsx')

    USJobTitle = Jan2018[Jan2018['Dimension Type'] == boxplot2]

    graphData = go.Box(
        x=USJobTitle['Dimension'],
        y=USJobTitle['Value'],
        marker=dict(color='green'),
        )
    
    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        title=boxplot2+' box plot in top US Cities',
        showlegend=False,
        autosize=False,
        width=1100,
        height=800,
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
            title=boxplot2
        )
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_USMPBox = plot(figure, output_type='div', include_plotlyjs=False)
    return plot_USMPBox

def GlassdoorPlot6(boxplot):
    Jan2018 = pd.read_excel('data/LPR_data-2018-01.xlsx')

    USMedianPayBox = Jan2018[Jan2018['Measure'] == boxplot]

    graphData = go.Box(
        x=USMedianPayBox['Metro'],
        y=USMedianPayBox['Value'],
        marker=dict(color='red'),
        )
    
    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        title=boxplot+' box plot in top US Cities',
        showlegend=False,
        autosize=False,
        width=1100,
        height=800,
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
            title=boxplot
        )
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_USMPBox = plot(figure, output_type='div', include_plotlyjs=False)
    return plot_USMPBox


def main():
    job_rows = Jobs.objects.all()
    print(job_rows)

main()