# Generated by Django 4.0.4 on 2023-09-17 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0005_channel_bl_channel_operator_alter_channel_chtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='config',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Конфигурация'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='operator',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Оператор'),
        ),
    ]
