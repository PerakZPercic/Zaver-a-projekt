from ..models import ForumInvite, ForumUser
from django.shortcuts import render
from django.http import HttpRequest
import pygal


def handle(req: HttpRequest):
    # chart = pygal.HorizontalBar()
    # chart.title = "Current invites vs Registered users"
    # chart.add("Invites", len(ForumInvite.objects.all()))
    # chart.add("Users", len(ForumUser.objects.all()))

    # {"chart": chart.render_data_uri()}
    return render(req, "home.html", {})
