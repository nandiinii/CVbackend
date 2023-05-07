# Generated by Django 4.2 on 2023-05-07 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option1', models.TextField()),
                ('option2', models.TextField()),
                ('option3', models.TextField()),
                ('option4', models.TextField()),
                ('answer', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('entered_answer', models.IntegerField(default=0)),
            ],
        ),
    ]