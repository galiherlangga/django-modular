from django.contrib.admin.options import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

from engine.models import ModuleRegistry
from engine.utils.module_loader import install_module, list_available_modules, uninstall_module, upgrade_module

@login_required
def module_list_view(request):
    available_modules = list_available_modules()
    installed_module_registries = ModuleRegistry.objects.filter(installed=True)
    installed_modules = {mod.name: mod for mod in installed_module_registries}
    return render(request, 'engine/module_list.html', {
        'installed_modules_map': installed_modules,
        'available_modules': available_modules
    })

@login_required
def install_module_view(request, module_name):
    if request.method == 'POST':
        try:
            install_module(module_name)
            messages.success(request, f"Module {module_name} installed successfully.")
        except Exception as e:
            messages.error(request, f"Failed to install module {module_name}: {str(e)}")
    return redirect(reverse("engine:module_list"))

@login_required
def upgrade_module_view(request, module_name):
    if request.method == 'POST':
        try:
            upgrade_module(module_name)
            messages.success(request, f"Module {module_name} upgraded successfully.")
        except Exception as e:
            messages.error(request, f"Failed to upgrade module {module_name}: {str(e)}")
    return redirect(reverse("engine:module_list"))

@login_required
def uninstall_module_view(request, module_name):
    if request.method == 'POST':
        try:
            uninstall_module(module_name)
            messages.success(request, f"Module {module_name} uninstalled successfully.")
        except Exception as e:
            messages.error(request, f"Failed to uninstall module {module_name}: {str(e)}")
    return redirect(reverse("engine:module_list"))