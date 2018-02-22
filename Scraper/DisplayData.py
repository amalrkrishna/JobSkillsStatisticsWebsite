import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from Site.models import *
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
    #print(df)
    graphData = go.Bar(
        x=df[0],
        y=df[1])
    
    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        showlegend=False,
        autosize=False
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_div = plot(figure, output_type='div', include_plotlyjs=False)
    '''return url'''
    return plot_div

def GlassdoorPlot1():
    Jan2018 = pd.read_excel('data/LPR_data-2018-01.xlsx')

    USMetro = Jan2018[Jan2018['Measure'] == 'Metro Median Pay']
    print(USMetro)

    graphData = go.Bar(
        x=USMetro['Metro'],
        y=USMetro['Value'])
    
    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        title='Median Pay in top US Cities',
        showlegend=False,
        autosize=False,
        width=500,
        height=400,
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
            title="Median Pay"
        )
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_USMetro = plot(figure, output_type='div', include_plotlyjs=False)
    print(plot_USMetro)
    return plot_USMetro

def GlassdoorPlot2():
    Jan2018 = pd.read_excel('data/LPR_data-2018-01.xlsx')

    USJobOpen = Jan2018[Jan2018['Measure'] == 'Job Openings']

    graphData = go.Bar(
        x=USJobOpen['Metro'],
        y=USJobOpen['Value'])
    
    '''url = py.plot([graphData], output_type='div', include_plotlyjs=False)'''
    graphLayout = go.Layout(
        title='Job Openings in top US Cities',
        showlegend=False,
        autosize=False,
        width=500,
        height=400,
        xaxis=dict(
            autorange=True,
        ),
        yaxis=dict(
            autorange=True,
            title="Job Openings"
        )
        )

    figure = go.Figure(data = [graphData], layout = graphLayout)
    plot_USJobOpen = plot(figure, output_type='div', include_plotlyjs=False)
    return plot_USJobOpen