from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username,phone, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")


        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, phone, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            phone=phone,

        )
        user.is_admin=True
        user.is_staff=True
        user.is_customer=False
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

    

  
class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    company_name=models.CharField(verbose_name="company name", max_length=100, unique=False)
    phone=models.CharField(verbose_name="phone", max_length=15)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # Role_Choices = (
    #         ('MULTI TEACHER', 'MULTI TEACHER'),
    #         ('PHYSICS TEACHER', 'PHYSICS TEACHER'),
    #         ('CHEMISTRY TEACHER', 'CHEMISTRY TEACHER'),
    #         ('BIOLOGY TEACHER', 'BIOLOGY TEACHER'),
    #         ('ENGLISH TEACHER', 'ENGLISH TEACHER'),
    #         ('CIVICS TEACHER', 'CIVICS TEACHER'),
    #         ('MATHEMATICS TEACHER', 'MATHEMATICS TEACHER'),
    #         ('HISTORY TEACHER', 'HISTORY TEACHER'),
    #         ('GEOGRAPHY TEACHER', 'GEOGRAPHY TEACHER'),
    #         ('KISWAHILI TEACHER', 'KISWAHILI TEACHER'),
    #     )

    # role=models.CharField(verbose_name="role", choices=Role_Choices, max_length=50)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=True)

    hide_email = models.BooleanField(default=True)

    


    USERNAME_FIELD="username"
    REQUIRED_FIELDS=['email','phone']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class ProductsUnit(models.Model):
    
    Unit = models.CharField(verbose_name="Unit", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=500,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Unit + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Products Unit"


class PeoplesCategories(models.Model):   
    CategoryName = models.CharField(verbose_name="Category Name", max_length=100,blank=False,null=False)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/Images/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Peoples Categories"

    def __str__(self):
        return self.CategoryName

class ProductsCategories(models.Model):
    Type = models.ForeignKey(PeoplesCategories,verbose_name="Type", on_delete=models.CASCADE, blank=True,null=True)   
    Unit = models.ForeignKey(ProductsUnit,verbose_name="Product Unit", on_delete=models.CASCADE, blank=True,null=True)
    CategoryName = models.CharField(verbose_name="Category Name", max_length=100,blank=False,null=False)
    Store = models.IntegerField(verbose_name="Quantity in Store",blank=True,null=True)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/Images/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products Categories"

    def __str__(self):
        return self.CategoryName


class OurServices(models.Model):   
    ServiceName = models.CharField(verbose_name="Service Name", max_length=100,blank=False,null=False)
    ServiceImage = models.ImageField(verbose_name="Service Image", upload_to='media/Images/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "OurServices"

    def __str__(self):
        return self.ServiceName


class ProductsFeatures(models.Model):   
    FeatureName = models.CharField(verbose_name="Feature", max_length=200,blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Product Features"

    def __str__(self):
        return self.FeatureName



class ProductsStores(models.Model):
    
    Unit = models.ForeignKey(ProductsUnit, verbose_name="Product Unit",on_delete=models.CASCADE, blank=True,null=True)
    productCategory = models.ForeignKey(ProductsCategories,verbose_name="Product Category",on_delete=models.CASCADE, blank=True,null=True)
    Type = models.ForeignKey(PeoplesCategories,verbose_name="Type",on_delete=models.CASCADE, blank=True,null=True)
    Feature = models.ForeignKey(ProductsFeatures, verbose_name="Feature",on_delete=models.CASCADE, blank=True,null=True)
    
    product_name = models.CharField(verbose_name="Product Name", max_length=100,blank=False,null=False)
    product_second_name = models.CharField(default="",verbose_name="Product Second Name", max_length=100,blank=True,null=True)

    InitialPrice = models.CharField(verbose_name="Initial Product price", max_length=200,blank=True,null=True)
    price = models.CharField(verbose_name="Main Price*", max_length=200,blank=True,null=True)
    #ProductUnit = models.CharField(verbose_name="Product Unit", max_length=100,blank=True,null=True)
    ProductQuantity = models.IntegerField(verbose_name="Product Quantity",blank=True,null=True)
    InitialProductQuantity = models.IntegerField(verbose_name="Initial Product Quantity*",blank=True,null=True)
    ProductImage = models.ImageField(verbose_name="Product Image", upload_to='media/ProductsInventoryImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        verbose_name_plural = "Stores"
        
    
    def __str__(self):
        return f" {self.product_name} {self.product_second_name} "


# @receiver(pre_save, sender=ProductsStores)
# def Products__initial_quantity(sender, **kwargs):
#     Initial_qty = kwargs['instance']
#     Initial_qty.InitialProductQuantity = Initial_qty.ProductQuantity
#     # total_cart_items = CartItems.objects.filter(user = cart_items.user )
#     # cart = Cart.objects.get(id = cart_items.cart.id)
#     # cart.total_price = cart_items.price
#     # cart.save()

@receiver(pre_save, sender=ProductsStores)
def set_initial_quantity(sender, instance, **kwargs):
    # Check if the instance is new (i.e., it doesn't have a primary key yet)
    if instance._state.adding:
        instance.InitialProductQuantity = instance.ProductQuantity

@receiver(pre_save, sender=ProductsStores)
def set_price_from_initial_price(sender, instance, **kwargs):
    # Check if the instance is new (i.e., it doesn't have a primary key yet)
    if instance._state.adding:
        instance.price = instance.InitialPrice

class ProductsCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(verbose_name="Total Price", default=0)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products  Cart"

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         


class ProductsCartItems(models.Model):
    cart = models.ForeignKey(ProductsCart, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductsStores,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    #Customer = models.ForeignKey(ProductsCustomers,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    #table = models.ForeignKey(ProductsTables,on_delete=models.CASCADE,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products  Cart Items"
    
    def __str__(self):
        return f" {self.product.product_name} {self.product.product_second_name} "
        
    

@receiver(pre_save, sender=ProductsCartItems)
def Products__correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = ProductsStores.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    # total_cart_items = CartItems.objects.filter(user = cart_items.user )
    # cart = Cart.objects.get(id = cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()



class ProductsOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    cart = models.ForeignKey(ProductsCart, on_delete=models.CASCADE, blank=True, null=True)
    # orderItems = models.ManyToManyField('ProductsOrderItems')
    total_price = models.FloatField(verbose_name="Total Price")

    CategoryId = models.IntegerField(verbose_name="Category ID",blank=True,null=True)
    closed_order_state = models.BooleanField(verbose_name="Is Order Closed ?", default=False,blank=True,null=True)
    Customer = models.CharField(max_length=500, verbose_name="Customer Name",blank=True,null=True)

    # table_number = models.CharField(max_length=500, verbose_name="Table Number",blank=True,null=True)

    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products Orders"

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class ProductsOrderItems(models.Model):
    order = models.ForeignKey(ProductsOrder, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductsStores,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    # Customer = models.ForeignKey(ProductsCustomers,on_delete=models.CASCADE,blank=True,null=True)
    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    # table = models.ForeignKey(ProductsTables,on_delete=models.CASCADE,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products Orders Items"

    def __str__(self):
        return f" {self.product.product_name} {self.product.product_second_name} " 


