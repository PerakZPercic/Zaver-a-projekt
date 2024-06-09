from django.contrib.staticfiles import finders
from django.http import HttpRequest
from django.shortcuts import render
from ..models import ProductModel
import json


def handle(req: HttpRequest, name: str):
    context = {
        "found_product": False,
        "product": None
    }

    try:
        product = ProductModel.objects.get(inner_name=name)
        result = finders.find(f"products/{name}.json")
        if result is not None:
            context["found_product"] = True
            context["product"] = product
            with open(result) as product_data:
                context["data"] = json.loads(product_data.read())

    except:
        pass

    return render(req, "product.html", context)
