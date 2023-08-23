from django.contrib.auth.models import Group
from django.shortcuts import render
from .seralizer import *
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from . import models
from rest_framework.response import Response
from django.contrib.auth.models import Group, User
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404


#! Some names might be different but the main functionality work 

class MenuList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = models.MenuItem.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MenuItemAddSera
        elif self.request.method == "PUT":
            return MenuItemAddSera2
        return super().get_serializer_class()

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            idItem = request.data.get("oldItemId")
            title = request.data.get("title")
            category_id = request.data.get("category")
            # Retrieve Category instance
            category = get_object_or_404(models.Category, id=category_id)
            back = get_object_or_404(models.MenuItem, id=idItem)

            back.title = title
            back.category = category  # Assign the Category instance
            back.save()

            return Response("Record updated successfully")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if self.request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            title = serializer.data.get('title')
            if models.MenuItem.objects.filter(title=title).exists():
                return Response("Item already exist")
            serializer.save()
            return Response("Item added successfully")
        return Response("You don't have permission")


class CatagoriesView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CataGoriesSera

    def get_queryset(self):
        queryset = models.Category.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CataGoriesAddSera
        return super().get_serializer_class()

    def post(self, request):
        if self.request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            title = request.data['title']
            print(title)
            if models.Category.objects.filter(title=title).exists():
                return Response("Item already exist")
            else:
                serializer.save()
            return Response("Item added successfully")
        return Response("You don't have permission")


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        my_group = Group.objects.get(name="Customers")
        user.groups.add(my_group)
        return Response({
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListUsers

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            queryset = User.objects.all()
            return queryset
        else:
            return User.objects.none()  # Return an empty queryset if the user is not a manager

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SetManager(generics.GenericAPIView):
    serializer_class = RegisterManager

    def post(self, request):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        if self.request.user.is_staff:
            userId = request.data.get("userId")
            if userId:
                user = User.objects.filter(id=userId).first()
                if user:
                    if not user.groups.filter(name="Manager").exists():
                        my_group = Group.objects.get(name="Manager")
                        user.groups.add(my_group)
                        return Response({"message": "This user is now a manager!"})
                    return Response({"message": "Already a manager"})
                else:
                    return Response({'error': 'User not found'}, status=404)
            else:
                return Response({'error': 'Missing credentials'}, status=400)
        return Response("Don't have permission")


class ListOrder(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSera
    ordering_fields = ['-price']

    def get_queryset(self):
        queryset = models.Order.objects.all()
        return queryset

    # def get_serializer_class(self):
    #     if self.request.method == "POST":
    #         return OrderDelSera
    #     return super().get_serializer_class()

    # * First display the orders for the specified user
    #! then create a post order

    def get(self, request):
        if self.request.user.groups.filter(name="Manager"):
            mod = models.Order.objects.values()
            return Response(mod)
        elif self.request.user.groups.filter(name="Customers"):
            id = self.request.user.id
            userMod = get_object_or_404(User, id=id)
            mod = models.Order.objects.filter(user=userMod).values()
            if len(mod) == 0:
                return Response("You don't have any orders")
            return Response(mod)
        else:
            return Response("Permission Denied")

    def post(self, request):
        if self.request.user.groups.filter(name="Customers").exists():
            # & First check for values
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                id = self.request.user.id
                userMod = get_object_or_404(User, id=id)
                print(userMod)
                mod = models.Order.objects.filter(user=userMod).values()
                print(mod)
                if len(mod) is not 0:
                    return Response("You already have a Pending cart")
                serializer.save()
                return Response("Cart created Successfully")
            return Response("Good morning")


class SpecCatagorieView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSera
    ordering_fields = ['-price']

    def get(self, request, cato):
        categoryModule = models.Category.objects.filter(title=cato).values()
        if len(categoryModule) == 0:
            return Response(f'(--{cato}--) Category does not exist')
        id = categoryModule[0]["id"]
        items = models.MenuItem.objects.filter(category=id).values()
        if len(items) == 0:
            return Response("List is empty")
        return Response(items)


class drivers(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeliveryCrewSera

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return OrderDelSera
        return super().get_serializer_class()

    def get(self, request):
        if request.user.groups.filter(name="Drivers").exists():
            id = self.request.user.id
            lists = get_object_or_404(models.DeliveryCrew, delivery_crew=id)
            serializer = DeliveryCrewSera(lists)
            print(lists)

            return Response(serializer.data)
        return Response("You are not a driver, Permission denied")

    def post(self, request):
        if request.user.groups.filter(name="Manager"):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            userId = request.data.get("order")
            delCrew = request.data.get("delivery_crew")
            userData = User.objects.get(id=delCrew)
            orderData = models.Order.objects.get(id=userId)
            if not models.DeliveryCrew.objects.filter(order=orderData, delivery_crew=userData).exists():
                dri = models.DeliveryCrew.objects.create(
                    order=orderData, delivery_crew=userData)
                user = User.objects.get(id=userData.id)
                cus = Group.objects.get(name="Drivers")
                user.groups.add(cus)
                return Response("Driver assigned")
            return Response("Driver already there")

        else:
            return Response("Permission denied")

    def put(self, request):
        if request.user.groups.filter(name="Drivers"):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                id = self.request.user.id
                statusData = request.data.get("status")
                updateState = get_object_or_404(
                    models.DeliveryCrew, delivery_crew=id)
                updateState.status = statusData
                updateState.save()
                return Response("Status Updated!")
            return Response("Missing field or Error")
        return Response("Permission Denied")


class CartView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSera

    def get(self, request):
        if self.request.user.groups.filter(name="Customers").exists() or self.request.user.is_staff:
            id = self.request.user.id
            mod = get_object_or_404(User, id=id)
            cart = models.Cart.objects.filter(user=mod)
            if len(cart) == 0:
                return Response("Not found")
            return Response(cart.values())

    def post(self, request):
        if self.request.user.groups.filter(name="Customers").exists() or self.request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                id = self.request.user.id
                menuId = request.data['menuitem']
                userMod = get_object_or_404(User, id=id)
                itemMod = get_object_or_404(models.MenuItem, id=menuId)

                itemToSave = models.Cart.objects.filter(menuitem=menuId)

                if len(itemToSave) is not 0:
                    return Response("This item already exists in cart")
                newItem = models.Cart.objects.create(
                    user=userMod, menuitem=itemMod, quantity=request.data['quantity'], unit_price=request.data['unit_price'], price=request.data['price'])
                return Response("Item added to cart!")
