# Generated by Django 5.0 on 2024-02-09 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_feedback_sellerid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='seller',
            field=models.IntegerField(default=0),
        ),
    ]
