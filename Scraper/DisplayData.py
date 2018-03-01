import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from Site.models import *
from Scraper import preprocessing
from Scraper import scraper
from Scraper import DisplayData
import os


def GetSkillsFromJobRegion(job, region):
    job_skills = JobSkill.objects.filter(category = job).all()
    
    job_skill_return = []
    for job_skill in job_skills:
        skill = job_skill.skill
        try:
            job_skill_count = JobSkillCount.objects.get(job_skill_id = job_skill.id)
            job_skill_return.append((skill, job_skill_count.posted_count))
        except:
            job_skill_return.append((skill, 0))
        
    df = pd.DataFrame( [[ij for ij in i] for i in job_skill_return] )
    print(df[0])
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