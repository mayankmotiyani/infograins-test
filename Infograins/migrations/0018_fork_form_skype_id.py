# Generated by Django 3.1.4 on 2022-05-27 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0017_fork_form_demo_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='fork_form',
            name='skype_id',
            field=models.CharField(default='', max_length=100),
        ),
    ]
