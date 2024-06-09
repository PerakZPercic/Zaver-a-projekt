from django.views.generic import ListView
from ..models import ProductModel


class ProductsListView(ListView):
    model = ProductModel
    template_name = "productList.html"
    context_object_name = "my_products"
    paginate_by = 8

    def get_queryset(self):
        return ProductModel.objects.all()
