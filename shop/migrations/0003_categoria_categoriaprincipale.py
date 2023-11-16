# Generated by Django 4.2.6 on 2023-11-16 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_prodotto_descrizione'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='categoriaPrincipale',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sottocategorie', to='shop.categoria'),
        ),
    ]
