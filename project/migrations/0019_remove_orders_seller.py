# Generated by Django 5.0.6 on 2024-06-24 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_cart_categoryid_cart_sellerid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='seller',
        ),
    ]
