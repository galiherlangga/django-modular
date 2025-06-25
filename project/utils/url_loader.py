import importlib
from django.urls import include, path, clear_url_caches
from engine.models import ModuleRegistry


def load_active_modules(urlpatterns):
    try:
        # Clear existing dynamic module URLs (keep only base URLs)
        base_patterns = [
            pattern for pattern in urlpatterns 
            if not (hasattr(pattern, 'pattern') and 
                   hasattr(pattern.pattern, '_route') and 
                   pattern.pattern._route.endswith('_module/'))
        ]
        
        # Replace urlpatterns with base patterns
        urlpatterns[:] = base_patterns
        
        # Add URLs for currently installed modules
        for module in ModuleRegistry.objects.filter(installed=True):
            try:
                url_module = importlib.import_module(f"{module.name}.urls")
                urlpatterns.append(path(f"{module.name}/", include(f"{module.name}.urls")))
                print(f"Loaded module: {module.name}")
            except ImportError as e:
                print(f"Failed to load module {module.name}: {e}")
        
        # Clear Django's URL cache to force it to reload patterns
        clear_url_caches()
        print(f"URL patterns reloaded. Total patterns: {len(urlpatterns)}")
        
    except Exception as e:
        print(f"Could not load active modules: {e}")
