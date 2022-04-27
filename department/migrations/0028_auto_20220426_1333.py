# Generated by Django 3.2.12 on 2022-04-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0027_auto_20220426_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='director_id',
            field=models.CharField(default='emp643', max_length=70),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp953', max_length=70),
        ),
        migrations.AlterField(
            model_name='employee',
            name='marital_status',
            field=models.CharField(choices=[('SINGLE', 'SINGLE'), ('MARRIED', 'MARRIED'), ('DIVORCED', 'DIVORCED')], max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='religion',
            field=models.CharField(choices=[('CHRISTIAN', 'CHRISTIAN'), ('MUSLIM', 'MUSLIM'), ('OTHER', 'OTHER')], max_length=255),
        ),
    ]
