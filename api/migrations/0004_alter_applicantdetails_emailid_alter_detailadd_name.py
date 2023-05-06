# Generated by Django 4.2.1 on 2023-05-05 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_detailadd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantdetails',
            name='EmailID',
            field=models.ForeignKey(max_length=254, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='detailadd',
            name='name',
            field=models.ForeignKey(max_length=25, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]