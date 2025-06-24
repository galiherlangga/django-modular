from rest_framework import serializers

from product_module.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def create(self, validated_date):
        print("Creating product with data:", validated_date)
        name = validated_date.get('name')
        barcode = validated_date.get('barcode')
        price = validated_date.get('price')
        stock = validated_date.get('stock', 0)
        
        try:
            price = float(price)
            stock = int(stock)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid data type for price or stock.")
        
        if not barcode.isalnum():
            raise serializers.ValidationError("Barcode must be alphanumeric.")
        if not name:
            raise serializers.ValidationError("Name cannot be empty.")
        if not price:
            raise serializers.ValidationError("Price is required.")
        if price < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        if stock < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        product = self.Meta.model.objects.create(**validated_date)
        
        return product
        
    def update(self, instance, validated_data):
        print("Updating product with data:", validated_data)
        for attr, value in validated_data.items():
            if attr == 'price':
                try:
                    value = float(value)
                    if value < 0:
                        raise serializers.ValidationError("Price cannot be negative.")
                except (ValueError, TypeError):
                    raise serializers.ValidationError("Invalid data type for price.")
            elif attr == 'stock':
                try:
                    value = int(value)
                    if value < 0:
                        raise serializers.ValidationError("Stock cannot be negative.")
                except (ValueError, TypeError):
                    raise serializers.ValidationError("Invalid data type for stock.")
            setattr(instance, attr, value)
        instance.save()
        return instance
        