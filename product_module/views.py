from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from product_module.serializers import ProductSerializer
from project.access.mixins import RoleRequiredMixin
from .models import Product

class ProductView(RoleRequiredMixin, View):
    allowed_roles = ['manager', 'user']
    
    def get_role(self, user):
        for role in self.allowed_roles:
            if user.groups.filter(name=role).exists():
                return role
        return 'public'
        
    def get(self, request, pk=None, action=None):
        role = self.get_role(request.user)
        
        if pk and action == "edit" and role in ['manager', 'user']:
            product = get_object_or_404(Product, pk=pk)
            return render(request, 'product_module/form.html', {'product': product, 'role': role})
        elif action == "create" and role in ['manager', 'user']:
            return render(request, 'product_module/form.html', {'product': None, 'role': role})
        
        products = Product.objects.all()
        return render(request, 'product_module/list.html', {'products': products, 'role': role})
    
    @method_decorator(csrf_protect)
    def post(self, request, pk=None, action=None):
        role = self.get_role(request.user)
        
        if action == "create" and role in ['manager', 'user']:
            serializer = ProductSerializer(data=request.POST)
            if serializer.is_valid():
                product = serializer.save()
                messages.success(request, "Product created successfully.")
                return redirect('product_module:product_list')
            else:
                messages.error(request, "Error creating product: " + str(serializer.errors))
                return render(request, 'product_module/form.html', {'product': serializer.data, 'role': role})
        
        elif pk and action == "edit" and role in ['manager', 'user']:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product, data=request.POST, partial=True)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, "Product updated successfully.")
                return redirect('product_module:product_list')
            else:
                messages.error(request, "Error updating product: " + str(serializer.errors))
                return render(request, 'product_module/form.html', {'product': serializer.data, 'role': role})
        
        elif pk and action == "delete" and role == "manager":
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            messages.success(request, "Product deleted successfully.")
            return redirect('product_module:product_list')
        
        messages.error(request, "Invalid action or insufficient permissions.")
        return render(request, 'product_module/list.html', {'role': role})