# Generated by Django 3.2.12 on 2022-04-13 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('department', '0009_alter_employee_emp_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='joined',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='employee',
            name='staff',
            field=models.OneToOneField(default=11, on_delete=django.db.models.deletion.CASCADE, to='user.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp911', max_length=70),
        ),
    ]
