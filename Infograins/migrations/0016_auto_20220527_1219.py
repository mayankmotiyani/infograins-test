# Generated by Django 3.1.4 on 2022-05-27 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0015_fork_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='fork_form',
            name='country_code',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='fork_form',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
    ]