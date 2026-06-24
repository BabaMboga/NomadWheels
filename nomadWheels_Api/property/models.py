import uuid
from django.conf import settings
from django.db import models

from user.models import User
# Create your models here.

class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()

    #pricing
    price_per_day = models.IntegerField(help_text="Rental priceperday in smallest currency uni")

    #vehicle specs
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20)
    color = models.CharField(max_length=50)

    #capacity & features
    seats = models.IntegerField()
    guests = models.IntegerField()
    transmission = models.CharField(
        max_length=20,
        choices=[
            ('automatic','Automatic'),
            ('manual', 'Manual'),
            ('cvt', 'CVT'),
        ],
        default='automatic'
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=[
            ('petrol', 'Petrol'),
            ('diesel', 'Diesel'),
            ('electric', 'Electric'),
            ('hybrid', 'Hybrid'),
            ('plugin_hybrid', 'Plug-in Hybrid'),
        ],
        default='petrol'
    )

    #Location
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    address = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=[
            ('economy', 'Economy'),
            ('compact', 'Compact'),
            ('mid_size', 'Mid_size'),
            ('full_size', 'Full_size'),
            ('luxury', 'Luxury'),
            ('suv', 'Suv'),
            ('van/minivan', 'Van/Minivan'),
            ('truck', 'Truck'),
            ('convertible', 'Convertible'),
            ('electric', 'Electric'),
        ],
        default = 'economy'
    )
    # favorited
    image = models.ImageField(upload_to='uploads/properties')
    landlord = models.ForeignKey(User,related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)