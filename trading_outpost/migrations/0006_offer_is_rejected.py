# Generated by Django 3.2.9 on 2021-12-12 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_outpost', '0005_alter_offer_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
