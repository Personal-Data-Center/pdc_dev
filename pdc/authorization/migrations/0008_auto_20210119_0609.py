# Generated by Django 3.1.4 on 2021-01-19 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0007_auto_20210119_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='profilePicSize4',
            field=models.CharField(default='defaultProfile.svg', max_length=150),
        ),
    ]
