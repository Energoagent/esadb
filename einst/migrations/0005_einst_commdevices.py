# Generated by Django 4.0.4 on 2023-09-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commdevice', '0006_remove_commdevice_einst'),
        ('einst', '0004_einst_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='einst',
            name='commdevices',
            field=models.ManyToManyField(to='commdevice.commdevice'),
        ),
    ]
