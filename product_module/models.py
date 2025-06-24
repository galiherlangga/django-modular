from django.db import models
from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    # name, barcode, price, stock
    name = models.CharField(max_length=255, unique=True)
    barcode = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def delete(self, using=None, keep_parents=False):
        """
        Override the delete method to set deleted_at instead of actually deleting the record.
        """
        self.deleted_at = now()
        self.save(update_fields=['deleted_at'])
        
    def restore(self):
        """
        Restore the product by setting deleted_at to None.
        """
        self.deleted_at = None
        self.save()
    
    def is_deleted(self):
        """
        Check if the product is deleted.
        """
        return self.deleted_at is not None