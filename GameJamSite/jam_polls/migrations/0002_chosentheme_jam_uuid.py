# Generated by Django 5.1.1 on 2024-11-09 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jam_polls', '0001_initial'),
        ('jams', '0007_uploadfile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chosentheme',
            name='jam_uuid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jams.gamejams'),
            preserve_default=False,
        ),
    ]