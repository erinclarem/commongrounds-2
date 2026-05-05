from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView

urlpatterns = [
    path('requests', CommissionListView.as_view(), name='commission-list'),
    path('request/add', CommissionCreateView.as_view(), name='commission-create'),
    path('request/<int:pk>', CommissionDetailView.as_view(), name='commission-detail'),
    path('request/<int:pk>/edit', CommissionUpdateView.as_view(), name='commission-update'),
]

app_name = 'commissions'
