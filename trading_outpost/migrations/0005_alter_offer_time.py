# Generated by Django 3.2.9 on 2021-12-11 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_outpost', '0004_alter_trade_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]