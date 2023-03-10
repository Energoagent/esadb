# Generated by Django 4.0.4 on 2022-11-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('docstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('inn', models.CharField(blank=True, max_length=10, null=True, serialize=False, verbose_name='ИНН')),
                ('req', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Реквизиты')),
                ('addr', models.CharField(blank=True, max_length=256, null=True, verbose_name='Адрес')),
                ('contactinfo', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Контакты')),
                ('info', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Общая информация')),
                ('note', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Примечание')),
                ('docs', models.ManyToManyField(to='docstore.docstore')),
            ],
            options={
                'verbose_name': 'Организация, юридическое лицо, ИП',
            },
        ),
    ]
