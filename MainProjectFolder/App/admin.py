from django.contrib import admin
from App.models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin

class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'phone', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username','phone', 'first_name', 'middle_name', 'last_name', 'company_name', 'phone', 'password1', 'password2'),
        }),
    )

    ordering=('email',)






class PeoplesCategoriesAdmin(admin.ModelAdmin):
    list_display = ["id","CategoryName","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]


class ProductsCategoriesAdmin(admin.ModelAdmin):
    list_display = ["id","CategoryName","Type", "Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]

class OurServicesAdmin(admin.ModelAdmin):
    list_display = ["id","ServiceName","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["ServiceName"]

class ProductsUnitAdmin(admin.ModelAdmin):
    list_display = ["id", "Unit","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Unit"]

class ProductsFeaturesAdmin(admin.ModelAdmin):
    list_display = ["id", "FeatureName", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["FeatureName"]



@admin.register(ProductsStores)
class ProductsStoresAdmin(ImportExportModelAdmin):
    list_display = ["id","product_name","product_second_name","productCategory","Type", "Feature", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]

#---------------------Products  CART---------------------
class ProductsCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class ProductsCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(ProductsOrder)  
class ProductsOrderAdmin(ImportExportModelAdmin):
    list_display = ["Customer","total_price", "created"]
    list_filter =["created"]
    search_fields = ["Customer"]

@admin.register(ProductsOrderItems)
class ProductsOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]



admin.site.register(MyUser, MyUserAdmin)
admin.site.register(ProductsCategories, ProductsCategoriesAdmin)
admin.site.register(OurServices, OurServicesAdmin)
admin.site.register(ProductsUnit, ProductsUnitAdmin)
admin.site.register(ProductsFeatures, ProductsFeaturesAdmin)
admin.site.register(PeoplesCategories, PeoplesCategoriesAdmin)



admin.site.register(ProductsCart, ProductsCartAdmin)
admin.site.register(ProductsCartItems, ProductsCartItemsAdmin)


