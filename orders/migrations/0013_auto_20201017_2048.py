# Generated by Django 3.1 on 2020-10-17 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_merge_20201017_2027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestorders',
            name='active',
        ),
        migrations.RemoveField(
            model_name='requestorders',
            name='quantity_type',
        ),
    ]