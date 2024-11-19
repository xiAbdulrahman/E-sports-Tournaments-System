import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    # ---------------------------Attributes---------------------------------------
    team = models.CharField(max_length=20, null=True, help_text="Team name")
    is_inTeam = models.BooleanField(default=False)
    is_TeamLeader = models.BooleanField(default=False)

    # ---------------------------Methods---------------------------------------
    def __str__(self):
        return self.username


class Team(models.Model):
    # ---------------------------Attributes---------------------------------------

    team_name = models.CharField(max_length=20, help_text="Team name")
    teamLeader = models.CharField(max_length=20, help_text="Team leader name")
    member1 = models.CharField(max_length=20,  null=True,help_text="first member",blank=True)
    member2 = models.CharField(max_length=20, null=True, help_text="second member",blank=True)
    member3 = models.CharField(max_length=20, null=True, help_text="third member",blank=True)
    member4 = models.CharField(max_length=20, null=True, help_text="fourth member",blank=True)
    member5 = models.CharField(max_length=20, null=True, help_text="fifth member", blank=True)
    is_inTournament = models.BooleanField(default=False)
    tournament_ID = models.IntegerField(null=True, help_text="" ,blank=True)
    team_Code = models.CharField(max_length=20, null=False, help_text="Team code")

# ---------------------------Methods---------------------------------------
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved (i.e., a new instance)
            while True:
                proposed_code = str(random.randint(100000, 999999))
                if not Team.objects.filter(team_Code=proposed_code).exists():
                    self.team_Code = proposed_code
                    break
        super().save(*args, **kwargs)

    def add_member(self, member_name):
        if self.member1 is None:
            self.member1 = member_name
        elif self.member2 is None:
            self.member2 = member_name
        elif self.member3 is None:
            self.member3 = member_name
        elif self.member4 is None:
            self.member4 = member_name
        elif self.member5 is None:
            self.member5 = member_name
        else:
            raise ValueError("Team is already full")

    def is_full(self):
        return all([self.member1, self.member2, self.member3, self.member4, self.member5])

    '''def kick_member(self, member_name):
        members = (self.member1, self.member2, self.member3, self.member4)
        for member in members:
            if member =='''

    def __str__(self):
        return self.team_name


# Tournament table
class Tournament(models.Model):
    # ---------------------------Attributes---------------------------------------
    teams = models.ManyToManyField(Team, related_name='tournaments', blank=True)
    maxPlayers = models.IntegerField(default=16)
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(help_text="End date")
    prize = models.IntegerField(help_text="prize")
    game = models.CharField(max_length=20, help_text="Game")
    is_full = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='tournaments/photos/', help_text="upload photo")
    first_round_matches_created = models.BooleanField(default=False)
    second_round_matches_created = models.BooleanField(default=False)
    third_round_matches_created = models.BooleanField(default=False)
    fourth_round_matches_created = models.BooleanField(default=False)

    # ----------------------------------Round1-----------------------------------------
    round1match1 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M1', null=True, blank=True)
    round1match2 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M2', null=True, blank=True)
    round1match3 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M3', null=True, blank=True)
    round1match4 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M4', null=True, blank=True)
    round1match5 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M5', null=True, blank=True)
    round1match6 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M6', null=True, blank=True)
    round1match7 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M7', null=True, blank=True)
    round1match8 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R1M8', null=True, blank=True)

    # ----------------------------------Round2-------------------------------------------
    round2match1 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R2M1', null=True, blank=True)
    round2match2 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R2M2', null=True, blank=True)
    round2match3 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R2M3', null=True, blank=True)
    round2match4 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R2M4', null=True, blank=True)
    # ----------------------------------Round3-------------------------------------------

    round3match1 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R3M1', null=True, blank=True)
    round3match2 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R3M2', null=True, blank=True)
    # ----------------------------------Round4-------------------------------------------

    round4match1 = models.ForeignKey("Match", on_delete=models.CASCADE, related_name='R4M1', null=True, blank=True)

    # ---------------------------Methods---------------------------------------
    def fill_round1_matches(self):

        if not self.first_round_matches_created:
            if self.teams.count() >= 3 and not self.first_round_matches_created:  # Ensuring at least 3 teams are available
                # Assuming teams are sorted, you may need to sort them accordingly.
                team_list = list(self.teams.all())

                # Creating Match objects for round 1
                match1 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[0],
                    team2=team_list[1],
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                match2 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[2],
                    team2=team_list[3],
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                match3 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[4],
                    team2=team_list[5],
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                match4 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[6],
                    team2=team_list[7],
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                match5 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[8],
                    team2=team_list[9],
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                match6 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[10],
                    team2=team_list[11],
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                match7 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[12],
                    team2=team_list[13],
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                match8 = Match.objects.create(
                    tournament=self,
                    round=1,
                    team1=team_list[14],
                    team2=team_list[15],
                    match_start_date=self.start_date  # Adjust as per requirement
                )

                # Assigning these matches to respective fields

                self.round1match1 = match1
                self.round1match2 = match2
                self.round1match3 = match3
                self.round1match4 = match4
                self.round1match5 = match5
                self.round1match6 = match6
                self.round1match7 = match7
                self.round1match8 = match8
                self.first_round_matches_created = True
                self.save()

    # ---------------------------Methods---------------------------------------
    def fill_round2_matches(self):

        if not self.second_round_matches_created:
            if self.teams.count() >= 3 and not self.second_round_matches_created:
                r2match1 = Match.objects.create(
                    tournament=self,
                    round=2,
                    team1= self.round1match1.winner,
                    team2= self.round1match2.winner,
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                r2match2 = Match.objects.create(
                    tournament=self,
                    round=2,
                    team1=self.round1match3.winner,
                    team2=self.round1match4.winner,
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                r2match3 = Match.objects.create(
                    tournament=self,
                    round=2,
                    team1=self.round1match5.winner,
                    team2=self.round1match6.winner,
                    match_start_date=self.start_date  # Adjust as per requirement
                )
                r2match4 = Match.objects.create(
                    tournament=self,
                    round=2,
                    team1=self.round1match7.winner,
                    team2=self.round1match8.winner,
                    match_start_date=self.start_date  # Adjust as per requirement
                )

                self.round2match1 = r2match1
                self.round2match2 = r2match2
                self.round2match3 = r2match3
                self.round2match4 = r2match4
                self.second_round_matches_created = True
                self.save()

    def fill_round3_matches(self):
        if not self.third_round_matches_created:
            if self.teams.count() >= 3 and not self.third_round_matches_created:
                r3match1 = Match.objects.create(
                    tournament=self,
                    round=3,
                    team1= self.round2match1.winner,
                    team2= self.round2match2.winner,
                    match_start_date=self.start_date
                )
                r3match2 = Match.objects.create(
                    tournament=self,
                    round=3,
                    team1=self.round2match3.winner,
                    team2=self.round2match4.winner,
                    match_start_date=self.start_date
                )

                self.round3match1 = r3match1
                self.round3match2 = r3match2

                self.third_round_matches_created = True
                self.save()

    def fill_round4_matches(self):
        if not self.fourth_round_matches_created:
            if self.teams.count() >= 3 and not self.fourth_round_matches_created:
                r4match1 = Match.objects.create(
                    tournament=self,
                    round=4,
                    team1= self.round3match1.winner,
                    team2= self.round3match2.winner,
                    match_start_date=self.start_date  # Adjust as per requirement
                )

                self.round4match1 = r4match1
                self.fourth_round_matches_created = True
                self.save()

    def refreshRound(self):
        self.round2match1.team1 = self.round1match1.winner
        self.round2match1.team2 = self.round1match2.winner
        self.round2match1.save()

        self.round2match2.team1 = self.round1match3.winner
        self.round2match2.team2 = self.round1match4.winner
        self.round2match2.save()

        self.round2match3.team1 = self.round1match5.winner
        self.round2match3.team2 = self.round1match6.winner
        self.round2match3.save()

        self.round2match4.team1 = self.round1match7.winner
        self.round2match4.team2 = self.round1match8.winner
        self.round2match4.save()

        self.round3match1.team1 = self.round2match1.winner
        self.round3match1.team2 = self.round2match2.winner
        self.round3match1.save()

        self.round3match2.team1 = self.round2match3.winner
        self.round3match2.team2 = self.round2match4.winner
        self.round3match2.save()

        self.round4match1.team1 = self.round3match1.winner
        self.round4match1.team2 = self.round3match2.winner
        self.round4match1.save()

    def __str__(self):
        return f"{self.game} - {self.id}"


class Match(models.Model):
    # ---------------------------Attributes---------------------------------------

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    round = models.IntegerField(help_text="prize",null=True,blank=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches', null=True, blank=True)
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches', null=True, blank=True)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winning_matches', blank=True, null=True)
    match_start_date = models.DateTimeField(help_text="Match start date and time")

    # ---------------------------Methods---------------------------------------

    def __str__(self):
        return f"{self.team1} vs {self.team2} "










