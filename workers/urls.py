from django.urls import path
from django.shortcuts import redirect
from workers import views

app_name = 'workers'
urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing_page'),
    # path('bewerben/', views.ApplicationFormView.as_view(), name='apply'),
    path('fertig/', views.SuccessView.as_view(), name='success'),
    path('impressum/', views.SiteNoticeView.as_view(), name='site_notice'),
    path('datenschutz/', lambda request: redirect('https://stura-md.de/datenschutz/'), name='privacy_policy'),
    path('kontakt/', views. ContactView.as_view(), name='contact'),
    path('agb/', views.TermsView.as_view(), name='terms'),
]
