# Generated by Django 4.0.4 on 2022-12-12 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contact_contactinfo'),
        ('org', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='contacts',
            field=models.ManyToManyField(to='contact.contact'),
        ),
    ]
