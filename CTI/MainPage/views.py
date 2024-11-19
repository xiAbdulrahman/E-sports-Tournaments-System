from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.shortcuts import redirect
from .models import *


# Create your views here.


def main(request):
    return render(request, 'base.html')


def login_v(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or wherever you want
            return redirect('afterLogin')
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


@login_required()
def logout_v(request):
    logout(request)
    # Redirect to a specific page after logout
    return redirect('main')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        # Check if username or email is already used
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username is already taken'})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email is already registered'})

        # Create user
        user = CustomUser.objects.create_user(username, email, password1)
        user.save()
        return redirect('login')
    return render(request, 'register.html')










@login_required()
def afterLogin(request):
    return render(request, 'afterlogin.html')


@login_required
def createTeam(request):
    if request.method == 'POST':
        team_name = request.POST.get('teamtextbox')
        # Check if the user in team
        if request.user.is_inTeam or request.user.is_TeamLeader:
            return render(request, 'afterlogin.html', {'error': 'You are already in team.'})
        # Check if a team with the same name already exists
        if Team.objects.filter(team_name=team_name).exists():
            return render(request, 'createTeam.html', {'error': 'Team name is already taken.'})
        else:
            # Create a new team instance
            team = Team.objects.create(
                team_name=team_name,
                teamLeader=request.user.username,
            )
            # Update the user's attributes
            request.user.is_inTeam = True
            request.user.is_TeamLeader = True
            request.user.team = team_name
            request.user.save()
            # Optionally, update the team leader field if needed
            team.teamLeader = request.user.username
            team.save()
            # Redirect to a success page or render a success message
            return redirect('myTeam')  # Replace 'success_page' with the name of your success page URL pattern
    return render(request, 'createTeam.html')  # Replace 'create_team.html' with the name of your template file
# ------------------------------------------------- Joining a TEAM -------------------------------------------


@login_required()
def joinTeam(request):
    if request.method == 'POST':
        team_code = request.POST.get('codeTextbox')
        # Check if the user is already in a team or is a team leader
        if request.user.is_inTeam or request.user.is_TeamLeader:
            return render(request, 'base.html', {'error': 'You are already in a team.'})
        try:
            team = Team.objects.get(team_Code=team_code)
        except Team.DoesNotExist:
            return render(request, 'joinTeam.html', {'error': 'Invalid team code.'})
        # Check if the team is full
        if team.is_full():
            return render(request, 'joinTeam.html', {'error': 'The team is full.'})
        # Assign the user to the team
        request.user.team = team.team_name
        request.user.is_inTeam = True
        # Update team members
        team.add_member(request.user.username)
        # Save changes
        request.user.save()
        team.save()
        return redirect('myTeam')  # Redirect to team dashboard or any other page
    return render(request, 'joinTeam.html')



@login_required()
def leaveTeam(request):
    team = Team.objects.filter(team_name=request.user.team).first()
    user = request.user
    if team.member1 == request.user.username:
        team.member1 = None
        user.is_inTeam = False
        user.is_TeamLeader = False
    elif team.member2 == request.user.username:
        team.member2 = None
        user.is_inTeam = False
        user.is_TeamLeader = False
    elif team.member3 == request.user.username:
        team.member3 = None
        user.is_inTeam = False
        user.is_TeamLeader = False
    elif team.member4 == request.user.username:
        team.member4 = None
        user.is_inTeam = False
        user.is_TeamLeader = False
    elif team.member5 == request.user.username:
        team.member5 = None
        user.is_inTeam = False
        user.is_TeamLeader = False
        # Save changes
    user.save()
    team.save()
    return render(request, 'base.html')  # Pass the team object to the template


@login_required()
def leave_promote1(request):
    if request.user.is_TeamLeader:
            user = request.user
            team = Team.objects.get(team_name=request.user.team)
            if team.member1 is not None:
                user.is_inTeam = False
                user.is_TeamLeader = False
                user.team = None
                user.save()
                team.teamLeader = team.member1
                team.member1 = None
                user1 = CustomUser.objects.get(username=team.teamLeader)
                user1.is_TeamLeader = True
                user1.save()
                team.save()
    return render(request, 'base.html')  # Pass the team object to the template

@login_required()
def leave_promote2(request):
    if request.user.is_TeamLeader:
        user = request.user
        team = Team.objects.get(team_name=request.user.team)
        if team.member2 is not None:
            user.is_inTeam = False
            user.is_TeamLeader = False
            user.team = None
            user.save()
            team.teamLeader = team.member2
            team.member2 = None
            user1 = CustomUser.objects.get(username=team.teamLeader)
            user1.is_TeamLeader = True
            user1.save()
            team.save()
    return render(request, 'base.html')  # Pass the team object to the template

@login_required()
def leave_promote3(request):
    if request.user.is_TeamLeader:
        user = request.user
        team = Team.objects.get(team_name=request.user.team)
        if team.member3 is not None:
            user.is_inTeam = False
            user.is_TeamLeader = False
            user.team = None
            user.save()
            team.teamLeader = team.member3
            team.member3 = None
            user1 = CustomUser.objects.get(username=team.teamLeader)
            user1.is_TeamLeader = True
            user1.save()
            team.save()
    return render(request, 'base.html')  # Pass the team object to the template

@login_required()
def leave_promote4(request):
    if request.user.is_TeamLeader:
        user = request.user
        team = Team.objects.get(team_name=request.user.team)
        if team.member4 is not None:
            user.is_inTeam = False
            user.is_TeamLeader = False
            user.team = None
            user.save()
            team.teamLeader = team.member4
            team.member4 = None
            user1 = CustomUser.objects.get(username=team.teamLeader)
            user1.is_TeamLeader = True
            user1.save()
            team.save()
    return render(request, 'base.html')  # Pass the team object to the template

@login_required()
def leave_promote5(request):
    if request.user.is_TeamLeader:
        user = request.user
        team = Team.objects.get(team_name=request.user.team)
        if team.member5 is not None:
            user.is_inTeam = False
            user.is_TeamLeader = False
            user.team = None
            user.save()
            team.teamLeader = team.member5
            team.member5 = None
            user1 = CustomUser.objects.get(username=team.teamLeader)
            user1.is_TeamLeader = True
            user1.save()
            team.save()
    return render(request, 'base.html')


@login_required()
def kick1(request):
    if request.user.is_TeamLeader:
        team = Team.objects.get(team_name=request.user.team)
        user = CustomUser.objects.get(username=team.member1)
        user.is_inTeam = False
        user.team = None
        team.member1 = None
        team.save()
        user.save()
        return render(request, 'myTeam.html')


@login_required()
def kick2(request):
    if request.user.is_TeamLeader:
        team = Team.objects.get(team_name=request.user.team)
        user = CustomUser.objects.get(username=team.member2)
        user.is_inTeam = False
        user.team = None
        team.member2 = None
        team.save()
        user.save()
        return render(request, 'myTeam.html')


@login_required()
def kick3(request):
    if request.user.is_TeamLeader:
        team = Team.objects.get(team_name=request.user.team)
        user = CustomUser.objects.get(username=team.member3)
        user.is_inTeam = False
        user.team = None
        team.member3 = None
        team.save()
        user.save()
        return render(request, 'myTeam.html')

@login_required()
def kick4(request):
    if request.user.is_TeamLeader:
        team = Team.objects.get(team_name=request.user.team)
        user = CustomUser.objects.get(username=team.member4)
        user.is_inTeam = False
        user.team = None
        team.member4 = None
        team.save()
        user.save()
        return render(request, 'myTeam.html')

@login_required()
def kick5(request):
    if request.user.is_TeamLeader:
        team = Team.objects.get(team_name=request.user.team)
        user = CustomUser.objects.get(username=team.member5)
        user.is_inTeam = False
        user.team = None
        team.member5 = None
        team.save()
        user.save()
        return render(request, 'myTeam.html')


@login_required()
def deleteTeam(request):
    team = Team.objects.get(team_name=request.user.team)
    leader = CustomUser.objects.filter(username=team.teamLeader).first()
    user1 = CustomUser.objects.filter(username=team.member1).first()
    user2 = CustomUser.objects.filter(username=team.member2).first()
    user3 = CustomUser.objects.filter(username=team.member3).first()
    user4 = CustomUser.objects.filter(username=team.member4).first()
    user5 = CustomUser.objects.filter(username=team.member5).first()
    members = [leader, user1, user2, user3, user4,user5]
    for member in members:
        if member:
            member.team = None
            member.is_inTeam = False
            member.is_TeamLeader = False
            member.save()
    team.delete()
    return render(request, 'afterLogin.html')


@login_required()
def myTeam(request):
    if request.user.is_inTeam:
        team = Team.objects.filter(team_name=request.user.team).first()
        return render(request, 'myTeam.html', {'team': team})  # Pass the team object to the template
    else:
        return render(request, 'afterLogin.html')


def tournamentList(request):
    tournaments = Tournament.objects.all()
    team = Team.objects.filter(team_name=request.user.team).first()
    return render(request, 'tournamentList.html', {'tournaments': tournaments, 'team' : team})
def join_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Assuming the authenticated user is a team leader
            if request.user.is_TeamLeader:
                team = Team.objects.filter(team_name=request.user.team).first()
                team.is_inTournament = True
                team.tournament_ID = tournament.id
                team.save()
                # Add the team to the tournament
                tournament.teams.add(team)
                tournament.save()
                return redirect('tournamentList')  # Redirect to a success page or wherever appropriate
    return render(request, 'tournamentList.html', {'tournaments': Tournament.objects.all()})


def leave_tournament(request, tournament_id):
    if request.method == 'POST':
        tournament = Tournament.objects.get(id=tournament_id)
        team = Team.objects.filter(team_name=request.user.team).first()
        team.is_inTournament = False
        team.tournament_ID = None
        team.save()
        tournament.teams.remove(team)
        tournament.save()
        return redirect('tournamentList')  # Redirect to a success page or wherever appropriate
    return render(request, 'tournamentList.html', {'tournaments': Tournament.objects.all()})
def brackets_tournament(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    # Check if any of the round1match1 attributes are already set
    tournament.fill_round1_matches()
    tournament.fill_round2_matches()
    tournament.fill_round3_matches()
    tournament.fill_round4_matches()
    tournament.refreshRound()
    tournament.save()
    return render(request, 'Brackets.html', {'tournament': tournament})


