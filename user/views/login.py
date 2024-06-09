from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from ..forms import ForumUserLoginForm
from django.http import HttpRequest


def handle(req: HttpRequest):
    context = {
        "err_type": -1
    }

    form = ForumUserLoginForm(req.POST or None)
    context["form"] = form

    if req.method == "POST":
        if form.is_valid():
            username = form.get_username()
            password = form.get_password()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                if req.GET.get("next") is not None:
                    return redirect(req.GET.get("next"))

                return redirect(f"/profile/{user.id}")

        context["err_type"] = 0

    return render(req, "login.html", context)
