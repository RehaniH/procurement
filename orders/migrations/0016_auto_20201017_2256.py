# Generated by Django 3.1 on 2020-10-17 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20201017_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestorders',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.orderstatus'),
        ),
    ]
