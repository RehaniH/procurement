# Generated by Django 3.1 on 2020-10-14 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=50)),
                ('note', models.CharField(max_length=150)),
                ('date', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=13)),
                ('employee_type', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=50)),
                ('address_line2', models.CharField(max_length=50)),
                ('address_line3', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('abbv', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=50)),
                ('company_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.location')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('quantity_type', models.CharField(max_length=15)),
                ('reorder_level', models.IntegerField(blank=True, default=10, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.item')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=15)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.location')),
            ],
        ),
        migrations.CreateModel(
            name='RequestOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('expected_date', models.CharField(max_length=50)),
                ('comment', models.CharField(blank=True, max_length=50, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.item')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.site')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderstatus')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('quantity_type', models.CharField(blank=True, max_length=15, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('delivery_date', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.employee')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.item')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.requestorders')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.site')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orderstatus')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPrices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=50)),
                ('Supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.supplier')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.item')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.site'),
        ),
    ]