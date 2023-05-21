from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import ReviewForm
from .models import Review


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('review_success')


class ReviewCreateSuccessView(TemplateView):
    template_name = 'reviews/review_form_done.html'
