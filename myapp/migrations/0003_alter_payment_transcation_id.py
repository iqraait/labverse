# Generated by Django 5.2 on 2025-04-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_payment_transcation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transcation_id',
            field=models.CharField(blank=True, editable=False, help_text='Auto _generated transaction id', max_length=200),
        ),
    ]
