# Generated by Django 3.2.12 on 2022-04-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0011_alter_employee_emp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp984', max_length=70),
        ),
    ]
