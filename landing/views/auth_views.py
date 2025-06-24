from django.contrib.auth.views import LoginView
from django.urls import reverse


class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        groups = user.groups.values_list('name', flat=True)
        
        if 'manager' in groups or user.is_superuser:
            return reverse('engine:module_list')
        elif 'user' in groups:
            return reverse('public_page')
        else:
            return reverse('public_page')