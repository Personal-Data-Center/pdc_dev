# Generated by Django 3.1.4 on 2021-01-19 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0006_auto_20210119_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='profilePicSize1',
            field=models.CharField(default='defaultProfile.svg', max_length=150),
        ),
        migrations.AlterField(
            model_name='profilepic',
            name='profilePicSize2',
            field=models.CharField(default='defaultProfile.svg', max_length=150),
        ),
        migrations.AlterField(
            model_name='profilepic',
            name='profilePicSize3',
            field=models.CharField(default='defaultProfile.svg', max_length=150),
        ),
    ]