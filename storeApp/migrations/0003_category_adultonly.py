# Generated by Django 4.2.4 on 2023-08-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0002_alter_product_adultonly'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='adultOnly',
            field=models.BooleanField(default=1),
        ),
    ]