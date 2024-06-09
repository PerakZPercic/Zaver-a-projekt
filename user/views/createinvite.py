from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import ForumUser, ForumInvite


@login_required(login_url="/login")
def handle(req: HttpRequest):
    user: ForumUser = req.user
    if not user.is_authenticated:
        return render(req, "createinvite.html", {"valid": False, "msg": "Authentication failed"})

    context = {
        "valid": True,
        "msg": None
    }

    inv: ForumInvite = user.invite_created_by_user
    if inv is None:
        inv = ForumInvite()
        inv.created_by = user.id
        inv.save()

        user.invite_created_by_user = inv
        user.save()

    context["msg"] = inv.invitation_code

    return render(req, "createinvite.html", context)
