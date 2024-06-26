# Generated by Django 4.1.7 on 2023-02-21 23:14

from django.db import migrations, models
import workers.models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='available_since',
            field=models.TimeField(blank=True, null=True, verbose_name='Verfügbar ab'),
        ),
        migrations.AddField(
            model_name='worker',
            name='available_until',
            field=models.TimeField(blank=True, null=True, verbose_name='Verfügbar bis'),
        ),
        migrations.AddField(
            model_name='worker',
            name='is_barkeeper',
            field=models.BooleanField(default=False, verbose_name='Bist du Barkeeper?'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worker',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[workers.models.validate_ovgu_mail], verbose_name='E-Mail-Adresse'),
        ),
    ]
