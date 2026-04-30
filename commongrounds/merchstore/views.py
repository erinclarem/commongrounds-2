from .models import Product, Transaction
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'

    def get_queryset(self):
        return super().get_queryset()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_products'] = Product.objects.all()
        if self.request.user.is_authenticated:
            context['user_products'] = Product.objects.filter(owner=self.request.user.profile)
            context['all_products'] = Product.objects.exclude(owner=self.request.user.profile)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'product_create.html'
    fields = ['name', 'description', 'price']


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_update.html'
    fields = ['name', 'description', 'price']


class CartView(ListView):
    model = Product
    template_name = 'cart.html'


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions.html'