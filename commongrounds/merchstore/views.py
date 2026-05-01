from .models import Product, Transaction
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from .forms import TransactionForm, ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_products'] = Product.objects.all()
        if self.request.user.is_authenticated:
            context['user_products'] = Product.objects.filter(
                owner=self.request.user.profile
                )
            context['all_products'] = Product.objects.exclude(
                owner=self.request.user.profile
                )
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


class ProductCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    required_role = 'Market Seller'
    form_class = ProductForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'owner': self.request.user.profile}
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class ProductUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    required_role = 'Market Seller'
    form_class = ProductForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'owner': self.request.user.profile}
        return kwargs
    
    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class CartView(ListView):
    model = Product
    template_name = 'cart.html'


class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions.html'
