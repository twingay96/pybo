# Generated by Django 3.1.3 on 2023-06-03 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0009_auto_20230602_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='seen_cnt',
            field=models.PositiveIntegerField(default=0),
        ),
    ]