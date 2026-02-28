from .models import Product
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
