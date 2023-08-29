# Generated by Django 4.2.3 on 2023-08-28 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0005_order_orderitem_invoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theProduct', to='storeApp.product')),
            ],
        ),
    ]