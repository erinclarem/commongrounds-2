from django.views.generic import ListView, DetailView
from .models import Commission


class CommissionListView(ListView):
    model = Commission
    template_name = 'commission_list.html'


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commission_detail.html'
