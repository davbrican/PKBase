# Generated by Django 3.2.9 on 2021-12-26 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jornada',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='jornada',
            name='temporada',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='jornada',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='local',
        ),
        migrations.RemoveField(
            model_name='partido',
            name='visitante',
        ),
        migrations.DeleteModel(
            name='Equipo',
        ),
        migrations.DeleteModel(
            name='Jornada',
        ),
        migrations.DeleteModel(
            name='Partido',
        ),
        migrations.DeleteModel(
            name='Temporada',
        ),
    ]
