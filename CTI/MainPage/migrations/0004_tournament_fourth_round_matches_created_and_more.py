# Generated by Django 5.0.3 on 2024-04-12 08:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainPage', '0003_tournament_round2match1_tournament_round2match2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='fourth_round_matches_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournament',
            name='round3match1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R3M1', to='MainPage.match'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='round3match2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R3M2', to='MainPage.match'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='round4match1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='R4M1', to='MainPage.match'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='third_round_matches_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team1_matches', to='MainPage.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team2_matches', to='MainPage.team'),
        ),
    ]
