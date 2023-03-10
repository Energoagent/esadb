# Generated by Django 4.0.4 on 2022-12-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('docstore', '0002_alter_docstore_doctype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('chtype', models.CharField(max_length=200, verbose_name='Тип')),
                ('info', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Общая информация')),
                ('note', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Примечание')),
                ('docs', models.ManyToManyField(to='docstore.docstore')),
            ],
            options={
                'verbose_name': 'Канал связи',
            },
        ),
    ]
