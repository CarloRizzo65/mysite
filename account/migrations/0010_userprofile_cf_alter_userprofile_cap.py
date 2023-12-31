# Generated by Django 4.2.6 on 2023-11-16 10:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_userprofile_cap'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cf',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(code='invalid_registration', message='Inserisci un cap corretto', regex='(?i)[A-Z]{6}\\d{2}[A-Z]\\d{2}[A-Z]\\d{3}[A-Z]')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cap',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(code='invalid_registration', message='Inserisci un cap corretto', regex='[0-9]{5}')]),
        ),
    ]
