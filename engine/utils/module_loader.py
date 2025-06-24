import importlib
from django.conf import settings
from django.utils.timezone import now

from engine.models import ModuleRegistry

def load_module():
    return [app for app in settings.INSTALLED_APPS if hasattr(importlib.import_module(app), 'manifest.module_config')]
    
def list_available_modules():
    available = []
    for app in settings.INSTALLED_APPS:
        try:
            importlib.import_module(f"{app}.manifest.module_config")
            available.append(app)
        except ModuleNotFoundError:
            continue
    return available

def install_module(module_name):
    try:
        config = importlib.import_module(f"{module_name}.manifest.module_config")
    except ModuleNotFoundError:
        raise ImportError(f"Module {module_name} not found.")
    
    if hasattr(config, 'install'):
        config.install()
        ModuleRegistry.objects.update_or_create(
            name=module_name,
            defaults={'installed': True}
        )
        print(f"Module {module_name} installed successfully.")
    else:
        raise AttributeError(f"Module {module_name} does not have an install method.")

def upgrade_module(module_name):
    try:
        config = importlib.import_module(f"{module_name}.manifest.module_config")
    except ModuleNotFoundError:
        raise ImportError(f"Module {module_name} not found.")
    
    if hasattr(config, 'upgrade'):
        config.upgrade()
        ModuleRegistry.objects.update_or_create(
            name=module_name,
            defaults={'installed': True, "updated_at": now() }
        )
        print(f"Module {module_name} upgraded successfully.")
    else:
        raise AttributeError(f"Module {module_name} does not have an upgrade method.")

def uninstall_module(module_name):
    try:
        config = importlib.import_module(f"{module_name}.manifest.module_config")
    except ModuleNotFoundError:
        raise ImportError(f"Module {module_name} not found.")
        
    if hasattr(config, 'uninstall'):
        config.uninstall()
        ModuleRegistry.objects.update_or_create(
            name=module_name,
            defaults={'installed': False}
        )
        print(f"Module {module_name} uninstalled successfully.")
    else:
        raise AttributeError(f"Module {module_name} does not have an uninstall method.")
        
