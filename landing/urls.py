from django.urls import path

from landing.views.auth_views import RoleBasedLoginView
from landing.views.public_views import public_home_view



urlpatterns = [
    path("", public_home_view, name="public_page"),
    path("accounts/login/", RoleBasedLoginView.as_view(), name="login")
]