# Generated by Django 4.2.6 on 2023-11-10 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_slide_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='img',
            field=models.ImageField(blank=True, default='no-image.png', null=True, upload_to='img_slide/', verbose_name='Immagine da visualizzare'),
        ),
    ]