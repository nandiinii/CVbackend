# Generated by Django 4.2.1 on 2023-05-05 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('DOB', models.DateField()),
                ('Location', models.CharField(max_length=50)),
                ('JobRole', models.CharField(max_length=50)),
                ('Gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=6)),
                ('PhoneNo', models.CharField(max_length=10)),
                ('EmailID', models.EmailField(max_length=254)),
                ('LinkedIn', models.CharField(max_length=100)),
                ('ResumeFile', models.FileField(upload_to='')),
            ],
        ),
    ]