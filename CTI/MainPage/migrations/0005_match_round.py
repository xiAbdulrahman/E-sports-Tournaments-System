# Generated by Django 5.0.3 on 2024-04-12 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainPage', '0004_tournament_fourth_round_matches_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='round',
            field=models.IntegerField(blank=True, help_text='prize', null=True),
        ),
    ]