# Generated by Django 3.2.12 on 2022-04-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0031_auto_20220427_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='director_id',
            field=models.CharField(default='dir854', max_length=70),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp785', max_length=70),
        ),
    ]
