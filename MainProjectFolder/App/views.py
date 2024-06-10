from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import *

from django.http import HttpResponse
from datetime import datetime, timedelta
import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import os
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from App.serializers import *


#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from App.serializers import *

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view
from django.db.models import Sum
from django.db import transaction


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



def home(request):

    return render(request, 'App/home.html')








class GetPeopleCategoriesView(APIView):
    def get(self, request):
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            


            queryset = PeoplesCategories.objects.all(
                
                )

            # # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = PeoplesCategoriesSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetProductCategoriesView(APIView):
    def get(self, request):
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            #TypeId = int(request.query_params.get('id'))
            


            queryset = ProductsCategories.objects.all(
                # Type__id__icontains = TypeId
                )

            # # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = ProductsCategoriesSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class GetAllProductsInStoreView(APIView):
    def get(self, request):
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            categoryId = int(request.query_params.get('id'))
            TypeId = int(request.query_params.get('TypeId'))
            


            queryset = ProductsStores.objects.filter(
                productCategory__id__icontains = categoryId,
                Type__id__icontains = TypeId
                )

            # # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(queryset, request)

            serializer = ProductsStoresSerializer(page_items, many=True)

            response_data = {
                'queryset': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














#--------------------REST APIS-------------------------------






class ProductsCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = ProductsCart.objects.filter(user=user, ordered=False).first()
        queryset = ProductsCartItems.objects.filter(cart=cart)
        serializer = ProductsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART
#     EG: {
#     "product":1,
#     "quantity":500
# }
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = ProductsCart.objects.get_or_create(user=user, ordered=False)
        product = ProductsStores.objects.get(id=data.get('product'))

        # room = ProductsRooms.objects.get(id=data.get('room'))
        # table = ProductsTables.objects.get(id=data.get('table'))
        # Customer = ProductsCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = ProductsCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = ProductsCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = ProductsCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = ProductsCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = ProductsCart.objects.filter(user=user, ordered=False).first()
        queryset = ProductsCartItems.objects.filter(cart=cart)
        serializer = ProductsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)




#TO DELETE SELECTED CART ITEM
class ProductsDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = ProductsCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProductsCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class ProductsOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    

    #----------------MAKE ORDER --------------------
    def post(self, request):
        user = request.user
        data = request.data
        Customer = request.user.username
        

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = ProductsCart.objects.filter(user=user, ordered=False).first()

        #room = ProductsRooms.objects.get(id=data.get('room'))
        #table = ProductsTables.objects.get(id=data.get('table'))
        #Customer = ProductsCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the  product category ID from the cart items
        product_category_ids = set()  # Using a set to ensure unique category IDs
        cart_items = ProductsCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            product_category_ids.add(cart_item.product.productCategory.id)

        # Create the order
        # order = ProductsOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber)
        order = ProductsOrder.objects.create(Customer=Customer, user=user, total_price=total_price)
        
        # Assign the first category ID found to the Order CategoryId field
        if product_category_ids:
            order.CategoryId = product_category_ids.pop()
            order.save()

        total_cart_items = ProductsCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # table.TableStatus = False
        # table.save()

        # Retrieve cart items and add them to the order
        cart_items = ProductsCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            ProductsOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                # table=table,
                # Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(ProductsOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = ProductsOrder.objects.filter(user=user)
    #     serializer = ProductsOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            CategoryId = int(request.query_params.get('CategoryId'))
            orders = ProductsOrder.objects.filter(
                user=user,
                CategoryId=CategoryId
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = ProductsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


















#------------------THIS IS FOR ADMIN--------------------------


#---------------------------TO FILTER ORDERS------------------



class FilterProductsOrdersView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        # userId = int(request.query_params.get('id'))
        CategoryId = int(request.query_params.get('CategoryId'))

        

        # Filter orders based on date range
        orders = RestaurantOrder.objects.filter(
            # user__id__icontains = userId,
            CategoryId=CategoryId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = ProductsOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)








#------------------GET ALL PRODUCTS ORDERS--------------

class GetAllProductsOrdersView(APIView):
    
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            # userId = int(request.query_params.get('id'))
            CategoryId = int(request.query_params.get('CategoryId'))

            orders = ProductsOrder.objects.filter(
                closed_order_state=False,
                # user__id__icontains = userId,
                CategoryId=CategoryId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = ProductsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#----------------ALL CLOSED BILLS------------------

class ClosedProductsOrdersView(APIView):
    
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            # userId = int(request.query_params.get('id'))
            CategoryId = int(request.query_params.get('CategoryId'))

            orders = ProductsOrder.objects.filter(
                closed_order_state=True,
                # user__id__icontains = userId,
                CategoryId=CategoryId

                ).order_by('-id')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = ProductsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#----------------GET ALL ORDERED ITEMS ----------------------

class GetAllProductsOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = ProductsOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = ProductsOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------DELETE Restaurant  ORDERED ITEMS---------------------
class DeleteProductsOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = ProductsOrderItems.objects.get(id=cartId)
            plus_order = ProductsOrderItems.objects.get(id=cartId)
            change_order_status = ProductsOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            #NI KWA AJILI YA KUCHANGE ORDER STATUS STATUS
            OrderId = int(request.query_params.get('id'))
            items_count= ProductsOrderItems.objects.filter(
                order__id__icontains = OrderId
                ).count()
            print(f"ORDER COUNT {items_count}")

            if items_count == 1:      
                #Change Table Status
                change_order_status.order.order_status = False
                change_order_status.order.closed_order_state = False
                change_order_status.order.save()

            #MWISHO NI KWA AJILI YA KUCHANGE TABLE STATUS


            order_item.delete()
 
            


            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except ProductsOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#---------------------------- COUNT ORDERS-------------------

class CountProductsOrderView(APIView):
    def get(self, request):
        try:
            _pending_orders = ProductsOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            _approved_orders = ProductsOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            _pending_orders_serializer = ProductsOrderSerializer(
                ProductsOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            _approved_orders_serializer = ProductsOrderSerializer(
                ProductsOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                '_pending_orders': _pending_orders,
                '_approved_orders': _approved_orders,
                '_pending_orders_data': _pending_orders_serializer.data,
                '_approved_orders_data': _approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ProductsOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        

#---------------- CLOSING BILL-------------------

class ProductsOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = ProductsOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            # ordered_items = ProductsOrderItems.objects.filter(order=order)
            # for item in ordered_items:
            #     item.table.TableStatus = False  # Update TableStatus to False
            #     item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except ProductsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









#--------------COUNT  ORDERS FOR SPECIFIC USER-----------------

class CountProductsOrdersForSpecificUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                #is_restaurant_user=True, 
                is_admin=False
                )
            user_data = []
            CategoryId = int(request.query_params.get('CategoryId'))

            for user in users:
                _pending_orders = ProductsOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    CategoryId=CategoryId
                    ).count()

                _approved_orders = ProductsOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    CategoryId=CategoryId
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "_pending_orders": _pending_orders,
                    "_approved_orders": _approved_orders,
                })

            serializer = ProductsOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






















#---------------------FOR CREATING DATA USING FUNCTION VIEW---------

#--------------------CREATE DATA ------------------------

class CreateNewItem(APIView):
    def post(self, request, format=None):
        serializer = AddProductsToStoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            #Send message to all user when new data is added
            queryset = MyUser.objects.all()
            for x in queryset:
                # Send an email to the user
                email = x.email
                subject = "Overdose Stores"
                message = f"Hello {x.username}, a new product has been added to the Overdose Stores App.\n \n Please visit our application to see more. \n \n Click on the link below to be the first. \n https://play.google.com/store/apps/details?id=ttpc.StudentsProjectsShare"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





