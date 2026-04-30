from .models import Product, Transaction
from accounts.mixins import RoleRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from .forms import TransactionForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'transaction_form' not in context:
            context['transaction_form'] = TransactionForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        transaction_form = TransactionForm(request.POST)

        if not request.user.is_authenticated:
            return redirect('accounts:login')

        if request.user.profile == self.object.owner:
            transaction_form.add_error(
                None, 'You cannot purchase your own product.'
                )
            return self.render_to_response(
                self.get_context_data(transaction_form=transaction_form)
            )

        if transaction_form.is_valid():
            if transaction_form.cleaned_data['amount'] > self.object.stock:
                transaction_form.add_error(
                    'amount', 'Not enough stock available.'
                    )
                return self.render_to_response(
                    self.get_context_data(transaction_form=transaction_form)
                )
            else:
                transaction = transaction_form.save(commit=False)
                transaction.buyer = request.user.profile
                transaction.product = self.object
                transaction.save()
                return redirect('cart')

        return self.render_to_response(
            self.get_context_data(transaction_form=transaction_form)
            )


class ProductCreateView(RoleRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    fields = '__all__'
    required_role = 'Market Seller'


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
