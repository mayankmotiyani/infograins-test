# Generated by Django 3.1.4 on 2022-03-22 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0004_auto_20220322_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mtag',
            name='Block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mtags', to='Infograins.blockchain'),
        ),
    ]
