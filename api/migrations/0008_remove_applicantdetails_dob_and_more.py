# Generated by Django 4.2.1 on 2023-05-05 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_detailadd_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicantdetails',
            name='DOB',
        ),
        migrations.RemoveField(
            model_name='applicantdetails',
            name='Gender',
        ),
        migrations.RemoveField(
            model_name='applicantdetails',
            name='JobRole',
        ),
        migrations.RemoveField(
            model_name='applicantdetails',
            name='Location',
        ),
        migrations.RemoveField(
            model_name='applicantdetails',
            name='Name',
        ),
    ]
