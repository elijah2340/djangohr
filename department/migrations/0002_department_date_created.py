# Generated by Django 3.2.12 on 2022-04-11 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
