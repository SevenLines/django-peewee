# Generated by Django 2.0.3 on 2018-03-11 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_django_peewee', '0008_testthroughmodel_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testthroughmodel',
            old_name='text',
            new_name='value',
        ),
    ]
