# Generated by Django 4.0.4 on 2022-12-12 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contact_contactinfo'),
        ('einst', '0002_einst_channels'),
    ]

    operations = [
        migrations.AddField(
            model_name='einst',
            name='contacts',
            field=models.ManyToManyField(to='contact.contact'),
        ),
    ]
