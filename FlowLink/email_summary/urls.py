from django.contrib import admin
from django.urls import path, include
from emails import views as email_views
from email_summary import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.login_view, name='login'),
    path('register/', main_views.register_view, name='register'),
    path('dashboard/', main_views.dashboard, name='dashboard'),
    path('logout/', main_views.logout_view, name='logout'),
    path('m_data/', main_views.m_data, name='m_data'),
    path('emails/<int:email_id>/', email_views.email_detail, name='email_detail'),
    path('authorize/', main_views.authorize, name='authorize'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('extract_emails/', main_views.extract_emails, name='extract_emails'),
    path('download_json/', main_views.download_json, name='download_json'),
    path('download_csv/', main_views.download_csv, name='download_csv'),
    path('download_excel/', main_views.download_excel, name='download_excel'),
]
