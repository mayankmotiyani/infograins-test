# Generated by Django 4.0.6 on 2022-07-07 11:10

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0020_blockchainschemas_servicesschema'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]
