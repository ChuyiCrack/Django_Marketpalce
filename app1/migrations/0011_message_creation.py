# Generated by Django 4.2.7 on 2023-11-25 19:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_product_description_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
