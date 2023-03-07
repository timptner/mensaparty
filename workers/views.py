from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from workers.forms import WorkerForm, ContactForm
from workers.models import Worker


class LandingPage(generic.TemplateView):
    template_name = 'workers/landing_page.html'


class ApplicationFormView(generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy('workers:success')


class SuccessView(generic.TemplateView):
    template_name = 'workers/success.html'


class SiteNoticeView(generic.TemplateView):
    template_name = 'workers/site_notice.html'


class ContactView(UserPassesTestMixin, generic.FormView):
    template_name = 'workers/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('admin:workers_worker_changelist')

    def test_func(self):
        return self.request.user.has_perm('workers.can_contact')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        workers = self.request.GET.get('workers')
        if workers:
            kwargs['initial'].update({'recipients': workers})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        workers = self.request.GET.get('workers')
        if workers:
            context['workers'] = Worker.objects.filter(pk__in=workers.split(',')).order_by('first_name', 'last_name')
        return context

    def form_valid(self, form):
        form.send_mail(self.request)
        return super().form_valid(form)


class TermsView(generic.TemplateView):
    template_name = 'workers/terms.html'
