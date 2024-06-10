from django.urls import path
from . import views

#app_name = "polls"

urlpatterns = [
    path('', views.home, name='home'),

    path('GetPeopleCategories/', views.GetPeopleCategoriesView.as_view(), name='GetPeopleCategories'),
    path('GetProductCategories/', views.GetProductCategoriesView.as_view(), name='GetProductCategories'),
    path('GetAllProductsInStore/', views.GetAllProductsInStoreView.as_view(), name='GetAllProductsInStore'),

    path('ProductsCart/', views.ProductsCartView.as_view(), name='ProductsCart'),
    path('ProductsOrder/', views.ProductsOrderView.as_view(), name='Products--order-list'),
    path('ProductsDeleteCartItem/', views.ProductsDeleteCartItemView.as_view(), name='ProductsDeleteCartItem'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),
    path('CreateNewItem/', views.CreateNewItem.as_view(), name='CreateNewItem'),



    #--------------TO FILTER ORDER--------------------------------
    path('FilterProductsOrders/', views.FilterProductsOrdersView.as_view(), name='FilterProductsOrders'),
    path('GetAllProductsOrders/', views.GetAllProductsOrdersView.as_view(), name='GetAllProductsOrders'),
    path('GetAllProductsOrderItems/', views.GetAllProductsOrderItemsView.as_view(), name='GetAllProductsOrderItems'),
    path('ClosedProductsOrders/', views.ClosedProductsOrdersView.as_view(), name='ClosedProductsOrders'),

    path('DeleteProductsOrderItem/', views.DeleteProductsOrderItemView.as_view(), name='DeleteProductsOrderItem'),
    path('CountProductsOrder/', views.CountProductsOrderView.as_view(), name='CountProductsOrder'),
    path('ProductsOrderCloseBill/', views.ProductsOrderCloseBillView.as_view(), name='ProductsOrderCloseBill'),
    path('CountProductsOrdersForSpecificUser/', views.CountProductsOrdersForSpecificUserView.as_view(), name='CountProductsOrdersForSpecificUser'),

   
        
]
