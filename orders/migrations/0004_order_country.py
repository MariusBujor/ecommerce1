# Generated by Django 3.2 on 2022-10-11 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
