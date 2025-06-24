from django.contrib.auth.mixins import LoginRequiredMixin

class RoleRequiredMixin:
    allowed_roles = []
    
    def test_func(self):
        return any(
            self.request.user.groups.filter(name=role).exists()
            for role in self.allowed_roles
        )