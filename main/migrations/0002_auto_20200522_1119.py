# Generated by Django 2.2.10 on 2020-05-22 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main',
            name='url',
            field=models.URLField(verbose_name='URL'),
        ),
    ]
