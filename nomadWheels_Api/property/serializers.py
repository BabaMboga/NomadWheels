from rest_framework import serializers
from .models import Property, PropertyImage, Booking

class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = [
            'id',
            'image',
            'image_url',
            'is_primary',
            'caption',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_image_url(self, obj):
        return obj.image_url
    
class PropertyListSerializer(serializers.ModelSerializer):
    """
        Lightweight serializer for list views ( search,results, homepage, cards etc.)
    """
    primary_image_url = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.get_full_name',read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'price_per_day',
            'make',
            'model',
            'year',
            'seats',
            'transmission',
            'fuel_type',
            'city',
            'country',
            'category',
            'primary_image_url',
            'owner_name',
            'is_available',
            'is_favorited',
            'created_at',
        ]

    def get_primary_image_url(self,obj):
        return obj.primary_image_url
    
    def get_is_favorited(self,obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favortied.filter(id=request.user.id).exists()
        return False
    
class PropertyDetailSerializer(serializers.ModelSerializer):
    """
        Full serializer for detail views with all relationships
    """
    images = PropertyImageSerializer(source='property_images', many=True,read_only=True)
    owner = serializers.SerializerMethodField()
    is_favortied = serializers.SerializerMethodField()
    favorited_count = serializers.IntegerField(source='favortied.count', read_only=True)
    bookings_count = serializers.IntegerField(source='bookings.count', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'price_per_day',
            'make',
            'model',
            'year',
            'license_plate',
            'color',
            'seats',
            'guests',
            'transmission',
            'fuel_type',
            'country',
            'country_code',
            'city',
            'address',
            'category',
            'images',
            'owner',
            'is_available',
            'is_insured',
            'is_favorited',
            'favorited_count',
            'bookings_count',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'owner']

    def get_owner(self,obj):
        return {
            'id': str(obj.owner.id),
            'name': obj.owner.get_full_name() or obj.owner.email,
            'email': obj.owner.email,
        }
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited.filter(id=request.user.id).exists()
        return False
    
class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating and updating properties
    """
    images = PropertyImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers. ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,

    )

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'price_per_day',
            'make',
            'model',
            'year',
            'license_plate',
            'color',
            'seats',
            'guests',
            'transmission',
            'fuel_type',
            'country',
            'country_code',
            'city',
            'address',
            'category',
            'images',
            'uploaded_images',
            'is_available',
            'is_insured',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        property_instance = Property.objects.create(**validated_data)

        for image in uploaded_images:
            PropertyImage.objects.create(property=property_instance,image=image)

        return property_instance
    
    def update(self,instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for image in uploaded_images:
            PropertyImage.objects.create(property=instance, image=image)

        return instance
    
class BookingSerializer(serializers.ModelSerializer):
    """
        Base booking serializer for listing user's bookings
    """
    property_title = serializers.CharField(source='property.title', read_only=True)
    primary_driver_name = serializers.CharField(source='primary_driver.get_full_name', read_only=True)
    additional_drivers_count = serializers.IntegerField(source='additional_drivers.count', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'property',
            'property_title',
            'start_date',
            'end_date',
            'pickup_time',
            'return_time',
            'number_of_days',
            'daily_rate',
            'total_price',
            'primary_driver',
            'primary_driver_name',
            'additional_drivers',
            'additional_drivers_count',
            'driver_age',
            'has_valid_license',
            'license_number',
            'license_expiry',
            'status',
            'mileage_at_pickup',
            'owner_review',
            'renter_review',
            'owner_rating',
            'renter_rating',
            'created_at',
            'upated_at',
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'primary_driver', 'status', 
            'number_of_days', 'total_price'
        ]

class BookingCreateSerializer(serializers.ModelSerializer):
    """
        Serializer for creating new bookings
    """

    class Meta:
        model = Booking
        fields = [
            'property',
            'start_date',
            'end_date',
            'pickup_time',
            'return_time',
            'driver_age',
            'has_valid_license',
            'license_number',
            'license_expiry',
        ]

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        
        # check for overlapping bookings
        overlapping = Booking.objects.filter(
            property=data['property'],
            status__in=['pending', 'confirmed', 'active'],
            start_date__lt=data['end_date'],
            end_date__gt=data['start_date']
        ).exists()

        if overlapping:
            raise serializers.ValidationError("Vehicle not available forselected dates.")
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        property_obj = validated_data['property']

        #calculate pricing 
        from datetime import datetime
        delta = validated_data['end_data'] - validated_data['start_date']
        number_of_days = delta.days

        validated_data['number_of_days'] = number_of_days
        validated_data['daily_rate'] = property_obj.price_per_day
        validated_data['total_price'] = number_of_days * property_obj.price_per_day
        validated_data['primary_driver'] = request.user
        validated_data['status'] = 'pending'

        return super().create(validated_data)

class BookingDetailSerializer(serializers.ModelSerializer):
    """
        Full booking detail with nested property info
    """
    property = PropertyListSerializer(read_only=True)
    primary_driver = serializers.SerializerMethodField()
    additional_drivers = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'property',
            'start_date',
            'end_date',
            'pickup_time',
            'return_time',
            'number_of_days',
            'daily_rate',
            'total_price',
            'primary_driver',
            'additional_drivers',
            'driver_age',
            'has_valid_license',
            'license_number',
            'license_expiry',
            'status',
            'mileage_at_pickup',
            'owner_review',
            'renter_review',
            'owner_rating',
            'renter_rating',
            'created_at',
            'upated_at',
        ]

    def get_primary_driver(self, obj):
        return {
            'id' : str(obj.primary_driver.id),
            'name': obj.primary_driver.get_full_name() or obj.primary_driver.email,
            'email': obj.primary_driver.email
        }
    
    def get_additional_drivers(self, obj):
        return [
            {
                'id': str(driver.id),
                'name' : driver.get_full_name() or driver.email,
                'email' : driver.email,
            }
            for driver in obj.additional_drivers.all()
        ]
        