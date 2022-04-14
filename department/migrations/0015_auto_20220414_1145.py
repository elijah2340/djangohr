# Generated by Django 3.2.12 on 2022-04-14 11:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0014_auto_20220414_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='hod',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp798', max_length=70),
        ),
    ]