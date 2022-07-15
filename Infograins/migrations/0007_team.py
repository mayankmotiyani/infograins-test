# Generated by Django 3.1.4 on 2022-04-06 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0006_auto_20220322_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=60, null=True)),
                ('designation', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='media')),
            ],
        ),
    ]