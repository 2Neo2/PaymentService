# Generated by Django 5.0.8 on 2024-08-19 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0002_merchantregistrationrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="merchantregistrationrequest",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="Email"),
        ),
    ]
