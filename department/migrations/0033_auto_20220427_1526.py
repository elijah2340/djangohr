# Generated by Django 3.2.12 on 2022-04-27 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0032_auto_20220427_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='name',
            field=models.CharField(default='JAy JAy', max_length=2000),
        ),
        migrations.AlterField(
            model_name='director',
            name='director_id',
            field=models.CharField(default='dir150', max_length=70),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp253', max_length=70),
        ),
    ]