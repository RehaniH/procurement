# Generated by Django 3.1 on 2020-10-16 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20201016_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverylog',
            name='qnty_type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='deliverylog',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]