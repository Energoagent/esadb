# Generated by Django 4.0.4 on 2023-09-17 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0002_alter_channel_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='iccid',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Идентификатор'),
        ),
        migrations.AddField(
            model_name='channel',
            name='ip',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='IP адрес: порт'),
        ),
        migrations.AddField(
            model_name='channel',
            name='number',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='chtype',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='info',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Информация'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование'),
        ),
    ]