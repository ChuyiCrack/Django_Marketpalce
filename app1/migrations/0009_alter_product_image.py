# Generated by Django 4.2.7 on 2023-11-22 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='./images'),
        ),
    ]
