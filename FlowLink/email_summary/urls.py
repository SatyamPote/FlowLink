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
    path('excel/', main_views.excel_view, name='excel_view'),
    path('download_json/', main_views.download_json, name='download_json'),
    path('download_csv/', main_views.download_csv, name='download_csv'),
]
