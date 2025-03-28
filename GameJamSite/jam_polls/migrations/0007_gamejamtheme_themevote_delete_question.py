# Generated by Django 5.1.6 on 2025-03-18 19:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jam_polls', '0006_delete_chosentheme'),
        ('jams', '0012_alter_game_options_alter_gamejam_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameJamTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=255)),
                ('gamejam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jams.gamejam')),
            ],
            options={
                'verbose_name': 'Тема джема',
                'verbose_name_plural': 'Темы джема',
            },
        ),
        migrations.CreateModel(
            name='ThemeVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField()),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jam_polls.gamejamtheme')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Голосование за тему',
                'verbose_name_plural': 'Голосования за тему',
            },
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
