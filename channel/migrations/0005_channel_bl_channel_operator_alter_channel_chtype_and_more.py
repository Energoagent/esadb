# Generated by Django 4.0.4 on 2023-09-17 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0004_rename_iccid_channel_ccid'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='bl',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Принадлежность'),
        ),
        migrations.AddField(
            model_name='channel',
            name='operator',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='IP адрес: порт'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='chtype',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='info',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Информация'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='note',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Примечание'),
        ),
    ]
