# Generated by Django 3.2.12 on 2022-04-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0012_alter_employee_emp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='HOD',
            field=models.CharField(default=22, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp945', max_length=70),
        ),
    ]
