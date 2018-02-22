import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from Site.models import *


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
