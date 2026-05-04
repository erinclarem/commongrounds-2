from multiprocessing import context
from .models import Project, Favorite
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from accounts.mixins import RoleRequiredMixin
from accounts.decorators import role_required
from .forms import ProjectRatingForm, ProjectForm, ProjectReviewForm, ProjectUpdateForm
from django.db.models import Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone


class ProjectListView(ListView):
    model = Project
    template_name = "projectlist.html"

    def get_queryset(self):
        queryset = Project.objects.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            queryset = queryset.exclude(creator=profile)
            queryset = queryset.exclude(favorites__profile=profile)
            queryset = queryset.exclude(reviews__reviewer=profile)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_projects'] = self.object_list

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['created_projects'] = Project.objects.filter(
                creator=profile
            ).distinct()
            context['favorited_projects'] = Project.objects.filter(
                favorites__profile=profile
            ).distinct()
            context['reviewed_projects'] = Project.objects.filter(
                reviews__reviewer=profile
            ).distinct()

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projectdetail.html"

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        avg_score = project.ratings.aggregate(avg_score=Avg('score'))
        context['favorite_count'] = project.favorites.count()
        context['avg_score'] = str(avg_score['avg_score'] or 0)
        context['reviews'] = project.reviews.all()

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['is_favorited'] = project.favorites.filter(profile=profile).exists()
            context['ProjectRatingForm'] = ProjectRatingForm()
            context['ProjectReviewForm'] = ProjectReviewForm()

        return context
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        project = self.object
        profile = request.user.profile

        if 'add_favorite' in request.POST:
            favorite = Favorite.objects.filter(
                project=project,
                profile=profile
            )

            if favorite.exists():
                favorite.delete()
            else:
                Favorite.objects.create(
                    project=project,
                    profile=profile,
                    date_favorited=timezone.now()
                )
            return redirect(self.get_success_url())

        if 'submit_rating' in request.POST:
            rating_form = ProjectRatingForm(request.POST)
            if rating_form.is_valid():
                if project.ratings.filter(profile=profile).exists():
                    project_rating = project.ratings.get(profile=profile)
                    project_rating.delete()
                rating = rating_form.save(commit=False)
                rating.profile = profile
                rating.project = project
                rating.save()
                return redirect(self.get_success_url())
            else:
                return self.render_to_response(
                    self.get_context_data(rating_form=rating_form)
                )

        elif 'submit_review' in request.POST:
            review_form = ProjectReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                if project.reviews.filter(reviewer=profile).exists():
                    project_review = project.reviews.get(reviewer=profile)
                    project_review.delete()
                review = review_form.save(commit=False)
                review.reviewer = profile
                review.project = project
                review.save()
                return redirect(self.get_success_url())
            else:
                return self.render_to_response(
                    self.get_context_data(review_form=review_form)
                )  

        return self.get(request, *args, **kwargs)  
    
    def get_success_url(self):
        return reverse_lazy('diyprojects:project_detail',
                            kwargs={'pk': self.kwargs['pk']})
        


class ProjectCreateView(RoleRequiredMixin, CreateView):
    required_role = "Project Creator"
    model = Project
    template_name = 'projectadd.html'
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        form.instance.project = self.object
        return super().form_valid(form)


class ProjectUpdateView(RoleRequiredMixin, UpdateView):
    required_role = "Project Creator"
    model = Project
    template_name = 'projectedit.html'
    form_class = ProjectUpdateForm

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user.profile)

    def get_success_url(self):
        return reverse_lazy('diyprojects:project_detail', kwargs={'pk': self.kwargs['pk']})
