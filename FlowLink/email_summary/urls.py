from django.contrib import admin
from django.urls import path
from emails import views as email_views
from email_summary import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.login_view, name='login'),
    path('register/', main_views.register_view, name='register'),
    path('dashboard/', main_views.dashboard, name='dashboard'),
    path('logout/', main_views.logout_view, name='logout'),
    path('emails/', email_views.email_list, name='email_list'),
    path('emails/<int:email_id>/', email_views.email_detail, name='email_detail'),
    path('authorize/', main_views.authorize, name='authorize'),
]
