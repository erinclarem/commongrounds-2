from .models import Commission, Job, JobApplication
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CommissionForm, JobApplicationForm, JobFormSet
 
 
class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/commission_list.html'
 
    def get_queryset(self):
        open_commissions = Commission.objects.filter(status='Open').order_by('-created_on')
        full_commissions = Commission.objects.filter(status='Full').order_by('-created_on')
        return list(open_commissions) + list(full_commissions)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_commissions = self.get_queryset()
        context['all_commissions'] = all_commissions
 
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
 
            my_commissions = [c for c in all_commissions if c.maker == profile]
 
            applied_ids = JobApplication.objects.filter(
                applicant=profile
            ).values_list('job__commission_id', flat=True)
            applied_commissions = [
                c for c in all_commissions
                if c.pk in applied_ids and c.maker != profile
            ]
 
            excluded_ids = set(c.pk for c in my_commissions) | set(c.pk for c in applied_commissions)
            context['my_commissions'] = my_commissions
            context['applied_commissions'] = applied_commissions
            context['all_commissions'] = [c for c in all_commissions if c.pk not in excluded_ids]
 
        return context
 
 
class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/commission_detail.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs = self.object.jobs.all()
 
        total_manpower = sum(job.manpower_required for job in jobs)
        accepted_total = sum(
            job.applications.filter(status=JobApplication.STATUS_ACCEPTED).count()
            for job in jobs
        )
 
        context['jobs'] = jobs
        context['total_manpower'] = total_manpower
        context['open_manpower'] = total_manpower - accepted_total
 
        if 'application_form' not in context:
            context['application_form'] = JobApplicationForm()
 
        return context
 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
 
        if not request.user.is_authenticated:
            return redirect('accounts:login')
 
        if request.user.profile == self.object.maker:
            return self.render_to_response(self.get_context_data())
 
        job_id = request.POST.get('job_id')
        try:
            job = self.object.jobs.get(pk=job_id)
        except Job.DoesNotExist:
            return self.render_to_response(self.get_context_data())
 
        if not job.is_full():
            JobApplication.objects.get_or_create(
                job=job,
                applicant=request.user.profile
            )
 
        return redirect(self.object.get_absolute_url())
 
 
class CommissionCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Commission
    template_name = 'commissions/commission_form.html'
    required_role = 'Commission Maker'
    form_class = CommissionForm
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            context['formset'] = JobFormSet()
        context['action'] = 'Create'
        return context
 
    def post(self, request, *args, **kwargs):
        self.object = None
        form = CommissionForm(request.POST)
        formset = JobFormSet(request.POST)
 
        if form.is_valid() and formset.is_valid():
            commission = form.save(commit=False)
            commission.maker = request.user.profile
            commission.save()
            formset.instance = commission
            formset.save()
            return redirect(commission.get_absolute_url())
 
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
 
 
class CommissionUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Commission
    template_name = 'commissions/commission_form.html'
    required_role = 'Commission Maker'
    form_class = CommissionForm
 
    def get_queryset(self):
        return Commission.objects.filter(maker=self.request.user.profile)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in context:
            context['formset'] = JobFormSet(instance=self.object)
        context['action'] = 'Update'
        return context
 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommissionForm(request.POST, instance=self.object)
        formset = JobFormSet(request.POST, instance=self.object)
 
        if form.is_valid() and formset.is_valid():
            commission = form.save()
            formset.save()
 
            all_jobs = commission.jobs.all()
            if all_jobs.exists() and all(job.status == Job.STATUS_FULL for job in all_jobs):
                commission.status = Commission.STATUS_FULL
                commission.save()
 
            return redirect(commission.get_absolute_url())
 
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
