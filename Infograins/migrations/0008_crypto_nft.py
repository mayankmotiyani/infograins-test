# Generated by Django 3.1.4 on 2022-04-15 05:21

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0007_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('Crypto_img', models.ImageField(blank=True, default='', null=True, upload_to='media')),
                ('para', ckeditor_uploader.fields.RichTextUploadingField(default='')),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NFT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('img', models.ImageField(blank=True, default='', null=True, upload_to='media')),
                ('para', ckeditor_uploader.fields.RichTextUploadingField(default='')),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
    ]
