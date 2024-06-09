from django.template import loader, Template
from django.http import HttpResponse


def handle(req, ex):
    template: Template = loader.get_template("404.html")
    return HttpResponse(template.render({}, req), status=404)
