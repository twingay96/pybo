# Generated by Django 3.1.3 on 2023-05-10 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='content',
            field=models.TextField(default='TextField'),
        ),
    ]
