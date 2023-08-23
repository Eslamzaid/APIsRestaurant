from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

# Register serializer
#! Some names might be different but the main functionality work

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], password=validated_data['password'])
        return user


class RegisterManager(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField()
    userId = serializers.IntegerField()


class ListUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # You can include more fields as needed


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MenuItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    featured = serializers.BooleanField()
    category = serializers.CharField()


class MenuItemAddSera(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['title', 'price', 'featured', 'category']


class MenuItemAddSera2(serializers.ModelSerializer):
    oldItemId = serializers.IntegerField()

    class Meta:
        model = models.MenuItem
        fields = ['title', 'price', 'featured', 'category', 'oldItemId']


class CataGoriesSera(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class CataGoriesAddSera(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['title', 'slug']


class DeliveryCrewSera(serializers.ModelSerializer):
    class Meta:
        model = models.DeliveryCrew
        fields = ['order', 'delivery_crew', 'status']


class OrderSera(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = "__all__"

class OrderDelSera(serializers.Serializer):
    status = serializers.CharField(max_length=50)


class OrderSpeCata(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = "__all__"
        

class CartSera(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'