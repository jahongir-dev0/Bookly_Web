# Generated by Django 4.2.18 on 2025-02-02 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_popular',
            field=models.BooleanField(default=False),
        ),
    ]
