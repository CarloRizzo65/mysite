# Generated by Django 4.2.6 on 2023-11-10 18:35

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_slide_contenuto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='contenuto',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]
