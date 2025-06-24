import importlib
from engine.models import ModuleRegistry


def installed_modules(request):
    modules = ModuleRegistry.objects.filter(installed=True)
    installed = []
    for mod in modules:
        try:
            module = importlib.import_module(mod.name)
            mod_path = getattr(module, '__file__', 'Unknown')
            installed.append({
                'name': ' '.join(word.capitalize() for word in mod.name.split('_')),
                'path': mod_path,
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