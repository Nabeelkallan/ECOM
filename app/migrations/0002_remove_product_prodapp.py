# Generated by Django 4.1.7 on 2023-08-10 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='prodapp',
        ),
    ]