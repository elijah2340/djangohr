# Generated by Django 3.2.12 on 2022-04-11 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0003_auto_20220411_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='bank',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp979', max_length=70),
        ),
        migrations.AlterField(
            model_name='employee',
            name='nuban',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]