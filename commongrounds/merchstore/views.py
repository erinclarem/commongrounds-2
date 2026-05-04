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
                self.object.stock -= transaction.amount
                
                if Transaction.objects.filter(
                    buyer=request.user.profile,
                    product=self.object,
                    status='on cart'
                    ).exists():
                    existing_transaction = Transaction.objects.get(
                        buyer=request.user.profile,
                        product=self.object,
                        status='on cart'
                    )
                    if existing_transaction.amount + transaction.amount > self.object.stock:
                        transaction_form.add_error(
                            'amount', 'Not enough stock available considering existing cart items.'
                            )
                        return self.render_to_response(
                            self.get_context_data(transaction_form=transaction_form)
                        )
                    existing_transaction.amount += transaction.amount
                    existing_transaction.save()
                else:
                    on_cart = Transaction(
                    buyer=request.user.profile,
                    product=self.object,
                    amount=transaction.amount,
                    status='on cart'
                    )
                    on_cart.save()
                if self.object.stock == 0:
                    self.object.status = 'out of stock'
                transaction.save()
                return redirect('merchstore:cart')

        return self.render_to_response(
            self.get_context_data(transaction_form=transaction_form)
            )


class ProductCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    required_role = 'Market Seller'
    form_class = ProductForm

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user.profile
        return initial

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class ProductUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    required_role = 'Market Seller'
    form_class = ProductForm

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user.profile)
    
    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'cart.html'

    def get_queryset(self):
        return Transaction.objects.filter(
            buyer=self.request.user.profile,
            status='on cart'
        ).select_related('product', 'product__owner')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_cart_items = {}
        for item in self.object_list:
            owner = item.product.owner
            if owner not in grouped_cart_items:
                grouped_cart_items[owner] = []
            grouped_cart_items[owner].append(item)
        context['grouped_cart_items'] = grouped_cart_items
        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions.html'

    def get_queryset(self):
        return Transaction.objects.filter(
            product__owner=self.request.user.profile
        ).exclude(status='on cart').select_related('buyer', 'product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_transactions = {}
        for transaction in self.object_list:
            buyer = transaction.buyer
            if buyer not in grouped_transactions:
                grouped_transactions[buyer] = []
            grouped_transactions[buyer].append(transaction)
        context['grouped_transactions'] = grouped_transactions
        return context
