# Generated by Django 5.2 on 2025-04-09 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_payment_success'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
