# Generated by Django 3.2.12 on 2022-04-13 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(upload_to='employee/profile_picture'),
        ),
    ]