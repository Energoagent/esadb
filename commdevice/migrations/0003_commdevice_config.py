# Generated by Django 4.0.4 on 2023-09-17 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commdevice', '0002_commdevice_addrtype_alter_commdevice_addr'),
    ]

    operations = [
        migrations.AddField(
            model_name='commdevice',
            name='config',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Конфигурация'),
        ),
    ]