# Generated by Django 3.1.4 on 2021-01-18 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_auto_20210118_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicekey',
            name='apiKey',
            field=models.CharField(max_length=67, unique=True),
        ),
    ]