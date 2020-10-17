# Generated by Django 3.1 on 2020-10-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20201016_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverylog',
            name='note',
        ),
        migrations.AlterField(
            model_name='requestorders',
            name='expected_date',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='requestorders',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
