# Generated by Django 3.2.9 on 2021-12-07 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_outpost', '0002_rename_postiion_card_position'),
        ('account', '0002_auto_20211207_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='deck',
            field=models.ManyToManyField(to='trading_outpost.Card'),
        ),
    ]
