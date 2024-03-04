from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Product,UserProfile,CartItems,Cart,Comment,Bids

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields="__all__"
        read_only_fields=["id"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
        read_only_fields=["id","created_date","user"]

class CartItemSerializer(serializers.ModelSerializer):
   total=serializers.IntegerField(read_only=True)
   product=ProductSerializer(read_only=True)
   class Meta:
      model=CartItems
      fields="__all__"
      read_only_field=["id",
                     "product",
                     "is_active",
                     "created_at",
                     "updated_at",
                     "cart",
                     ]
class CartSerializer(serializers.ModelSerializer):
    cart_items=CartItemSerializer(read_only=True,many=True)
    cart_total=serializers.IntegerField(read_only=True)
    user=serializers.StringRelatedField()

    class Meta:
        model=Cart
        fields="__all__"
        read_only_fields=[
            "user",
            "is_active",
            "created_at",
            "updated_at",
            "cart_items"
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"
        read_only_fields=["id",
                          "created_date",
                          "user",
                          "product",
                          ]

class BidsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bids
        fields="__all__"
        read_only_fields=["id",
                          "user",
                          "product",
                          ]