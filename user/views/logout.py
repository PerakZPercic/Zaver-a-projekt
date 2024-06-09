from django.contrib.auth import logout
from django.shortcuts import redirect


def handle(req):
    logout(req)
    return redirect("home")
