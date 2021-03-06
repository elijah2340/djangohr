# Generated by Django 3.2.12 on 2022-04-11 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0004_auto_20220411_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp103', max_length=70),
        ),
        migrations.AlterField(
            model_name='employee',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='employee/profile_picture'),
        ),
    ]
