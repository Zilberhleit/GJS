# Generated by Django 5.1.1 on 2024-10-10 10:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jams', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamejams',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gamejams',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
