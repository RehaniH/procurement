# Generated by Django 3.1 on 2020-10-16 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20201015_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemprices',
            old_name='Supplier',
            new_name='supplier',
        ),
        migrations.AlterField(
            model_name='orders',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.supplier'),
        ),
    ]