# Generated by Django 4.2.7 on 2025-07-06 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecoles', '0009_remove_preinscription_moyenne_nationale_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecoleimage',
            name='description',
        ),
        migrations.RemoveField(
            model_name='typeecole',
            name='description',
        ),
    ]
