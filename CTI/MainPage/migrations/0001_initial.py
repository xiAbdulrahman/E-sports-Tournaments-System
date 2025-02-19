# Generated by Django 5.0.3 on 2024-04-11 13:15

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(help_text='Team name', max_length=20)),
                ('teamLeader', models.CharField(help_text='Team leader name', max_length=20)),
                ('member1', models.CharField(blank=True, help_text='first member', max_length=20, null=True)),
                ('member2', models.CharField(blank=True, help_text='second member', max_length=20, null=True)),
                ('member3', models.CharField(blank=True, help_text='third member', max_length=20, null=True)),
                ('member4', models.CharField(blank=True, help_text='fourth member', max_length=20, null=True)),
                ('member5', models.CharField(blank=True, help_text='fifth member', max_length=20, null=True)),
                ('is_inTournament', models.BooleanField(default=False)),
                ('tournament_ID', models.IntegerField(blank=True, null=True)),
                ('team_Code', models.CharField(help_text='Team code', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_start_date', models.DateTimeField(help_text='Match start date and time')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1_matches', to='MainPage.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2_matches', to='MainPage.team')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winning_matches', to='MainPage.team')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maxPlayers', models.IntegerField(default=16)),
                ('start_date', models.DateField(help_text='Start date')),
                ('end_date', models.DateField(help_text='End date')),
                ('prize', models.IntegerField(help_text='prize')),
                ('game', models.CharField(help_text='Game', max_length=20)),
                ('is_full', models.BooleanField(default=False)),
                ('photo', models.ImageField(help_text='upload photo', upload_to='tournaments/photos/')),
                ('first_round_matches_created', models.BooleanField(default=False)),
                ('round1match1', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M1', to='MainPage.match')),
                ('round1match2', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M2', to='MainPage.match')),
                ('round1match3', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M3', to='MainPage.match')),
                ('round1match4', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M4', to='MainPage.match')),
                ('round1match5', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M5', to='MainPage.match')),
                ('round1match6', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M6', to='MainPage.match')),
                ('round1match7', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M7', to='MainPage.match')),
                ('round1match8', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='R1M8', to='MainPage.match')),
                ('teams', models.ManyToManyField(blank=True, related_name='tournaments', to='MainPage.team')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='MainPage.tournament'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('team', models.CharField(help_text='Team name', max_length=20, null=True)),
                ('is_inTeam', models.BooleanField(default=False)),
                ('is_TeamLeader', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
