from django.template import loader, Template
from django.http import HttpResponse
from ..models import ForumUser

from pygal.style import DarkStyle
import pygal


def handle(req, uid):
    user: ForumUser = None
    chart_uri = None

    try:
        user = ForumUser.objects.get(id=uid)

        chart = pygal.Pie(style=DarkStyle)
        chart.title = "User invite statistics"
        chart.add("Created", user.created_invites)
        chart.add("Used", user.used_invites)
        chart_uri = chart.render_data_uri()
    except:
        pass

    template: Template = loader.get_template("profile.html")
    exists: bool = user is not None

    context = {
        "exists": exists,
        "uid": exists and user.id or 0,
        "name": exists and user.username or "User not found",
        "is_banned": exists and user.is_banned or False,
        "chart": chart_uri
    }

    return HttpResponse(template.render(context, req))
