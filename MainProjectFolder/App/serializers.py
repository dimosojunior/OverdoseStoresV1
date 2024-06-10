from App.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from App.models import *


# from rest_framework.validators import UniqueValidator
# from rest_framework_jwt.settings import api_settings



#______________DJANGO REACT AUTHENTICATION_________________

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email','phone', 'password')

#______________MWISHO HAPA DJANGO REACT AUTHENTICATION_________________





class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
        # fields = ['id', 'username', 'email','phone','first_name','profile_image']












# kwa ajili ya kumregister mtu bila kutumia token
class UserCreationSerializer(serializers.ModelSerializer):
	username=serializers.CharField(max_length=25)
	email=serializers.EmailField(max_length=50)
	password=serializers.CharField(max_length=50)


	class Meta:
		model= MyUser
		fields= ['username','email','password']
		#fields='__all__'

	def validate(self,attrs):
		username_exists = MyUser.objects.filter(username=attrs['username']).exists()
		if username_exists:
			raise serializers.ValidationError(detail="User with username already exists")


		email_exists = MyUser.objects.filter(email=attrs['email']).exists()
		if email_exists:
			raise serializers.ValidationError(detail="User with email already exists")

		return super().validate(attrs)








class ProductsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsUnit
        fields = '__all__'


class ProductsCategoriesSerializer(serializers.ModelSerializer):
    Unit = ProductsUnitSerializer(many=False)
    class Meta:
        model = ProductsCategories
        fields = '__all__'

class PeoplesCategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PeoplesCategories
        fields = '__all__'

class OurServicesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OurServices
        fields = '__all__'
		

class ProductsStoresSerializer(serializers.ModelSerializer):
    Unit = ProductsUnitSerializer(many=False)
    productCategory = ProductsCategoriesSerializer(many=False)
    class Meta:
        model = ProductsStores
        fields = '__all__'

class AddProductsToStoreSerializer(serializers.ModelSerializer):
    # Unit = ProductsUnitSerializer(many=False)
    # productCategory = ProductsCategoriesSerializer(many=False)
    class Meta:
        model = ProductsStores
        fields = '__all__'

    def create(self, validated_data):
	    image_file = validated_data.pop('ProductImage', None)
	    stores = ProductsStores.objects.create(**validated_data)

	    if image_file:
	        stores.ProductImage = image_file
	    stores.save()
	    return stores




#---------------------  CART SERIALIZER---------


class ProductsCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsCart
        fields = '__all__'


class ProductsCartItemsSerializer(serializers.ModelSerializer):
    cart = ProductsCartSerializer()
    product = ProductsStoresSerializer()

    #table = ProductsTablesSerializer()
    class Meta:
        model = ProductsCartItems
        fields = '__all__'



class ProductsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOrder
        fields = '__all__'


class ProductsOrderItemsSerializer(serializers.ModelSerializer):
    order = ProductsOrderSerializer()
    product = ProductsStoresSerializer()

    # table = ProductsTablesSerializer()
    # Customer = ProductsCustomersSerializer()
    class Meta:
        model = ProductsOrderItems
        fields = '__all__'






#-----------GET CUSTOMERS ----------------
class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'


#--------------COUNT  ORDERS FOR SPECIFIC USER-----------------
class ProductsOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    _pending_orders = serializers.IntegerField()
    _approved_orders = serializers.IntegerField()

