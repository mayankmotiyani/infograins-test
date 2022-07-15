# Generated by Django 3.1.4 on 2022-04-19 13:05

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0008_crypto_nft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockchain',
            name='service_para',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_para',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_para',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_para',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_para',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]