from django.shortcuts import render, redirect



def leaderboard(request):
    return render(request, 'EV_LeaderBoard.html')

# Create your views here.
