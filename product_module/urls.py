from django.urls import path
from product_module.views import ProductView

app_name = "product_module"

urlpatterns = [
    path('', ProductView.as_view(), name='product_list'),
    path('create/', ProductView.as_view(), {'action': 'create'}, name='product_create'),
    path('<int:pk>/edit/', ProductView.as_view(), {'action': 'edit'}, name='product_update'),
    path('<int:pk>/delete/', ProductView.as_view(), {'action': 'delete'}, name='product_delete'),
]