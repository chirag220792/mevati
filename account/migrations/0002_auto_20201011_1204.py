# Generated by Django 3.1 on 2020-10-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact_no',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
