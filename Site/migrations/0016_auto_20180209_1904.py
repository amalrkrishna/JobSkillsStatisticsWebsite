# Generated by Django 2.0.1 on 2018-02-10 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0015_auto_20180209_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobskillcount',
            name='job_skill',
        ),
        migrations.DeleteModel(
            name='JobSkillCount',
        ),
    ]
