import threading

from django.contrib import admin


from .models import *
from django.contrib import admin
from .models import Tournament
import discord
from discord.ext import commands

admin.site.register(CustomUser)
admin.site.register(Team)


class MatchInline(admin.TabularInline):
    model = Match
    extra = 0  # Number of extra forms to display

class TournamentsAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # If creating a new object (add page)
            self.exclude = ('teams', 'round1match1', 'round1match2', 'round1match3', 'round1match4', 'round1match5',
                            'round1match6', 'round1match7', 'round1match8', 'round2match1', 'round2match2',
                            'round2match3', 'round2match4', 'round3match1', 'round3match2', 'round4match1',
                            'first_round_matches_created', 'second_round_matches_created', 'third_round_matches_created',
                            'fourth_round_matches_created', 'is_full')
        else:  # If editing an existing object
            self.exclude = ('teams', 'round1match1', 'round1match2', 'round1match3', 'round1match4', 'round1match5',
                            'round1match6', 'round1match7', 'round1match8', 'round2match1', 'round2match2',
                            'round2match3', 'round2match4', 'round3match1', 'round3match2', 'round4match1',
                            'first_round_matches_created', 'second_round_matches_created', 'third_round_matches_created',
                            'fourth_round_matches_created', 'is_full', 'maxPlayers')
        return super().get_form(request, obj, **kwargs)

    inlines = [MatchInline]
    actions = ['create_voice_channels']

    def create_channels(self, team_names, guild_id, token, category_name):
        bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

        @bot.event
        async def on_ready():
            guild = bot.get_guild(guild_id)
            category = await guild.create_category(category_name)
            for name in team_names:
                await guild.create_voice_channel(name, user_limit=6,category=category)
            await bot.close()

        bot.run(token)



admin.site.register(Tournament, TournamentsAdmin, namespace='MainPage')
admin.site.register(Match)




