from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from product_module.models import Product


def setup_roles():
    content_type = ContentType.objects.get_for_model(Product)
    
    manager, _ = Group.objects.get_or_create(name="manager")
    permission = Permission.objects.filter(content_type=content_type)
    manager.permissions.set(permission)
    
    user, _ = Group.objects.get_or_create(name="user")
    user_permissions = Permission.objects.filter(content_type=content_type, codename__in=["add_product", "change_product", "view_product"])
    user.permissions.set(user_permissions)


# TODO: Adjust for uninstall module
def remove_roles():
    Group.objects.filter(name__in=["manager", "user", "public"]).delete()