# Generated by Django 5.0.4 on 2024-05-06 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traders', '0005_alter_product_options_product_model_product_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkitem',
            name='debt',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='задолженность'),
        ),
    ]
