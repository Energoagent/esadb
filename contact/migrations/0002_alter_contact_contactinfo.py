# Generated by Django 4.0.4 on 2022-12-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contactinfo',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Контактная информация: телефон e-mail и тд'),
        ),
    ]
