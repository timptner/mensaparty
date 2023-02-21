from django.views import generic
from django.urls import reverse_lazy
from workers.forms import WorkerForm
from workers.models import Worker


class LandingPage(generic.TemplateView):
    template_name = 'workers/landing_page.html'


class ApplicationFormView(generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy('workers:success')


class SuccessView(generic.TemplateView):
    template_name = 'workers/success.html'
