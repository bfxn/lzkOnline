# Generated by Django 2.2.16 on 2020-11-03 08:55

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='adress',
            field=DjangoUeditor.models.UEditorField(default='', max_length=100, verbose_name='地址'),
        ),
    ]
