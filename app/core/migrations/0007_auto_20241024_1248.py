# Generated by Django 3.2.25 on 2024-10-24 12:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_answer_answer'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='user',
        #     name='age',
        #     field=models.PositiveIntegerField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='user',
        #     name='gender',
        #     field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=10),
        # ),
        # migrations.AddField(
        #     model_name='user',
        #     name='grade',
        #     field=models.CharField(blank=True, max_length=10),
        # ),
        migrations.AddField(
            model_name='user',
            name='major',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='student_id',
            field=models.IntegerField(default=200000000, unique=True, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)]),
        ),
    ]
