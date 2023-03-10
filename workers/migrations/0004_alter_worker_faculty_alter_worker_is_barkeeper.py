# Generated by Django 4.1.7 on 2023-03-10 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0003_alter_worker_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='faculty',
            field=models.CharField(choices=[('', '--- Auswählen ---'), ('EIT', 'Elektro- und Informationstechnik'), ('SSE', 'Humanwissenschaften'), ('COS', 'Informatik'), ('MEE', 'Maschinenbau'), ('MAT', 'Mathematik'), ('MED', 'Medizin'), ('NAS', 'Naturwissenschaften'), ('PSE', 'Verfahrens- und Systemtechnik'), ('ECM', 'Wirtschaftswissenschaften')], max_length=3, verbose_name='Fakultät'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='is_barkeeper',
            field=models.BooleanField(choices=[(True, 'Ja'), (False, 'Nein')], default=False, verbose_name='Bist du Barkeeper?'),
        ),
    ]
