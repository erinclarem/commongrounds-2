from .models import Project
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class ProjectListView(ListView):
    model = Project
    template_name = "projectlist.html"


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projectdetail.html"
