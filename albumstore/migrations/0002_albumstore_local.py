# Generated by Django 4.0.4 on 2023-05-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albumstore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='albumstore',
            name='local',
            field=models.BooleanField(default=True),
        ),
    ]
