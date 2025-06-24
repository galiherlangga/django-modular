from django.core.management import call_command

from product_module.manifest.roles import remove_roles, setup_roles

def install():
    call_command('makemigrations', 'product_module')
    call_command('migrate', 'product_module')
    print("Product module installed successfully.")

def upgrade():
    call_command('makemigrations', 'product_module')
    call_command('migrate', 'product_module')
    print("Product module upgraded successfully.")
    
def uninstall():
    remove_roles()
    