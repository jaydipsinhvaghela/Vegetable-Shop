# Generated by Django 4.1.13 on 2024-04-22 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_orders_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='phone_num',
            new_name='mobile_no',
        ),
        migrations.AddField(
            model_name='contact',
            name='userid',
            field=models.IntegerField(default=0),
        ),
    ]
