# Generated by Django 5.2 on 2025-04-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_payment_transcation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
