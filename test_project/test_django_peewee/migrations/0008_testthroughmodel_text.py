# Generated by Django 2.0.3 on 2018-03-11 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_django_peewee', '0007_testmodel_others_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='testthroughmodel',
            name='text',
            field=models.CharField(max_length=100, null=True),
        ),
    ]