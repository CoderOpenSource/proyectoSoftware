# Generated by Django 5.0.6 on 2024-06-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_jugador_jugador_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugador',
            name='jugador_id',
            field=models.CharField(default='1031B6FB', max_length=10, unique=True),
        ),
    ]
