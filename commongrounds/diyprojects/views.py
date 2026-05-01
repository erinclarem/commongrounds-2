from .models import Project
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import RoleRequiredMixin


class ProjectListView(ListView):
    model = Project
    template_name = "projectlist.html"

    def get_queryset(self):
        queryset = Project.objects.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            queryset = queryset.exclude(creator=profile)
            queryset = queryset.exclude(favorite__profile=profile)
            queryset = queryset.exclude(projectreview__reviewer=profile)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_projects'] = self.object_list

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['created_projects'] = Project.objects.filter(
                creator=profile
            )
            context['favorited_projects'] = Project.objects.filter(
                favorite__profile=profile
            ).distinct()
            context['reviewed_projects'] = Project.objects.filter(
                projectreview__reviewer=profile
            ).distinct()

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projectdetail.html"


class ProjectCreateView(RoleRequiredMixin, CreateView):
    required_role = "Project Creator"
    model = Project
    template_name = 'projectcreate.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
