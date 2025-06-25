import importlib
from engine.models import ModuleRegistry
from django.urls import reverse

from project.utils.url_loader import load_active_modules


def installed_modules(request):
    modules = ModuleRegistry.objects.filter(installed=True)
    installed = []
    for mod in modules:
        try:
            module = importlib.import_module(mod.name)
            mod_path = getattr(module, '__file__', 'Unknown')
            urls_module = importlib.import_module(f"{mod.name}.urls")
            first_route = None
            app_name = getattr(urls_module, 'app_name', None)
            url_path = None
            if hasattr(urls_module, 'urlpatterns'):
                first_route = urls_module.urlpatterns[0].name if urls_module.urlpatterns else None
            # complete url path
            if first_route and app_name:
                try:
                    url_path = reverse(f"{app_name}:{first_route}")
                except Exception as e:
                    print(f"Error generating link for {app_name}:{first_route}: {e}")
                    url_path = None
            installed.append({
                'name': ' '.join(word.capitalize() for word in mod.name.split('_')),
                'path': mod_path,
                'url': url_path,
            })
        except Exception as e:
            print(f"Error processing module {mod.name}: {e}")
            continue
    role = "public"
    if request.user.is_authenticated:
        groups = request.user.groups.values_list('name', flat=True)
        if "manager" in groups:
            role = "manager"
        elif "user" in groups:
            role = "user"
    result = {
        "request": request,
        "installed_modules": installed,
        "role": role,
    }
    return result