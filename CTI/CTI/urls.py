"""
URL configuration for CTI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import MainPage.views

urlpatterns = [

                  path('admin/', admin.site.urls, name='admin'),
                  path('', MainPage.views.main, name='main'),
                  path('login', MainPage.views.login_v, name='login'),
                  path('logout/', MainPage.views.logout_v, name='logout'),
                  path('reset_password',
                       auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"),
                       name="reset_password"),
                  path('reset_password_sent',
                       auth_views.PasswordResetDoneView.as_view(template_name="registration/reset_password_sent.html"),
                       name="password_reset_done"),
                  path('reset/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('password_reset_complete'),
                       template_name="registration/reset.html"),
                       name="password_reset_confirm"),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/reset_password_complete.html"),
                       name="password_reset_complete"),
                  path('register', MainPage.views.register, name="register"),
                  path('afterLogin', MainPage.views.afterLogin, name='afterLogin'),
                  path('joinTeam', MainPage.views.joinTeam, name='joinTeam'),
                  path('createTeam', MainPage.views.createTeam, name='createTeam'),
                  path('myTeam', MainPage.views.myTeam, name='myTeam'),
                  path('tournamentList', MainPage.views.tournamentList, name='tournamentList'),
                  path('leaveTeam', MainPage.views.leaveTeam, name='leaveTeam'),
                  path('leave_promote1', MainPage.views.leave_promote1, name='leave_promote1'),
                  path('leave_promote2', MainPage.views.leave_promote1, name='leave_promote2'),
                  path('leave_promote3', MainPage.views.leave_promote1, name='leave_promote3'),
                  path('leave_promote4', MainPage.views.leave_promote1, name='leave_promote4'),
                  path('leave_promote5', MainPage.views.leave_promote1, name='leave_promote5'),
                  path('kick1', MainPage.views.kick1, name='kick1'),
                  path('kick2', MainPage.views.kick2, name='kick2'),
                  path('kick3', MainPage.views.kick3, name='kick3'),
                  path('kick4', MainPage.views.kick4, name='kick4'),
                  path('kick5', MainPage.views.kick5, name='kick5'),
                  path('deleteTeam', MainPage.views.deleteTeam, name='deleteTeam'),
                  path('join-tournament/<int:tournament_id>/', MainPage.views.join_tournament, name='join_tournament'),
                  path('leave-tournament/<int:tournament_id>/', MainPage.views.leave_tournament,
                       name='leave_tournament'),
                  path('brackets_tournament/<int:tournament_id>/', MainPage.views.brackets_tournament,
                       name='brackets_tournament')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
