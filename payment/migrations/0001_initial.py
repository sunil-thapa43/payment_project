# Generated by Django 5.1.5 on 2025-02-06 07:15

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NavyaBaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImePayDetails',
            fields=[
                ('navyabasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payment.navyabasemodel')),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ref_id', models.CharField(max_length=20)),
                ('token_id', models.CharField(blank=True, max_length=20, null=True)),
                ('transaction_id', models.CharField(max_length=20)),
                ('msisdn', models.CharField(blank=True, max_length=20, null=True)),
                ('ime_transaction_status', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)])),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('response_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'IME Pay Details',
            },
            bases=('payment.navyabasemodel',),
        ),
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('navyabasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payment.navyabasemodel')),
                ('payment_partner', models.TextField(blank=True, choices=[('eSewa', 'ESEWA'), ('IME Pay', 'IME_PAY'), ('Khalti', 'KHALTI'), ('Connect IPS', 'CONNECT_IPS')], null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('purpose', models.CharField(blank=True, max_length=400, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=25)),
                ('amount_in_paisa', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('transaction_id', models.CharField(max_length=100)),
                ('status', models.TextField(choices=[('Initiated', 'INITIATED'), ('Completed', 'COMPLETED'), ('Failed', 'FAILED'), ('Cancelled', 'CANCELLED'), ('Error', 'ERROR')])),
                ('signature', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Payment Requests',
            },
            bases=('payment.navyabasemodel',),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('navyabasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payment.navyabasemodel')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_in_paisa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_id', models.CharField(max_length=100)),
                ('user_id', models.IntegerField()),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.paymentrequest')),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
            bases=('payment.navyabasemodel',),
        ),
    ]
