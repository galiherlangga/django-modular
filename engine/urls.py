

from django.urls import path

from engine import views


app_name = "engine"

urlpatterns = [
    path('', views.module_list_view, name='module_list'),
    path('install/<str:module_name>', views.install_module_view, name='install_module'),
    path('upgrade/<str:module_name>', views.upgrade_module_view, name='upgrade_module'),
    path('uninstall/<str:module_name>', views.uninstall_module_view, name='uninstall_module'),
]
