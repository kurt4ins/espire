from rest_framework import serializers
from mainapp.models import Brand, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "description")


class ProductSerializer(serializers.ModelSerializer):
    brand_info = BrandSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "brand",
            "brand_info",
            "description",
            "cost",
            "quantity",
            "img",
        )
