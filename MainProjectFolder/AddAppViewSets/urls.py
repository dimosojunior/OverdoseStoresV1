
from django.urls import path
from . import views

# # MWANZO IN ORDER TO USE MODEL VIEW SET
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('Customers', views.CustomersViewSet)
router.register('ProductsCategories', views.ProductsCategoriesViewSet)
router.register('ProductsUnit', views.ProductsUnitViewSet)
router.register('AddProductsToStore', views.AddProductsToStoreViewSet)
router.register('OurServices', views.OurServicesViewSet)
router.register('PeoplesCategories', views.PeoplesCategoriesViewSet)







urlpatterns = router.urls