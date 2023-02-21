from django.urls import path
from workers import views

app_name = 'workers'
urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing_page'),
    path('apply/', views.ApplicationFormView.as_view(), name='apply'),
    path('success/', views.SuccessView.as_view(), name='success'),
]
