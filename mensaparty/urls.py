from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from reviews.views import ReviewCreateView, ReviewCreateSuccessView

urlpatterns = [
    path('', include('workers.urls')),
    path('feedback/', ReviewCreateView.as_view(), name='review_create'),
    path('feedback/done/', ReviewCreateSuccessView.as_view(), name='review_success'),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
]
