# Generated by Django 3.2.12 on 2022-04-26 10:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0024_auto_20220425_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='actual_retirement',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='director',
            name='director_id',
            field=models.CharField(default='emp317', max_length=70),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp710', max_length=70),
        ),
    ]