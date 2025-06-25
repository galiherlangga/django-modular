from functools import wraps

from django.shortcuts import redirect

from engine.models import ModuleRegistry


def module_installed_required(module_name):
    def decorator(func):
        @wraps(func)
        def _wrapped_view(request, *args, **kwargs):
            if not ModuleRegistry.objects.filter(name=module_name, installed=True).exists():
                return redirect('public_page')
            return func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
