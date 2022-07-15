# Generated by Django 3.1.4 on 2022-03-22 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Infograins', '0003_auto_20220322_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_tag', models.TextField()),
                ('Block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Mtags', to='Infograins.blockchain')),
            ],
        ),
        migrations.DeleteModel(
            name='Mtags',
        ),
    ]