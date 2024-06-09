from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from ..models import ForumUser
from ..forms import ForumUserCreationForm
from django.http import HttpRequest


def handle(req: HttpRequest):
    context = {
        "err_type": -1
    }

    if req.method == "POST":
        form = ForumUserCreationForm(req.POST)

        (is_valid, err_type) = form.is_valid()
        if is_valid:
            username = form.get_username()
            password = form.get_password1()

            user = ForumUser.objects.create_user(username, form.get_email(), password, err_type)
            auth_user = authenticate(username=username, password=password)
            login(req, user)

            return redirect(f"/profile/{user.id}")

        # The default is_valid didn't pass (Username already taken, or password is too weak)
        if err_type == 0:
            form.cleaned_data["username"] = ""
            form.cleaned_data["password1"] = ""
            form.cleaned_data["password2"] = ""

        # Email already in use
        if err_type == 1:
            form.cleaned_data["email"] = ""

        # Invite code invalid
        if err_type == 2:
            form.cleaned_data["invite_code"] = ""

        context["err_type"] = err_type
        context["form"] = form
    else:
        context["form"] = ForumUserCreationForm()

    return render(req, "register.html", context)
