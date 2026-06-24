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

    # relationships
    favorited = models.ManyToManyField(User, related_name='favorite_vehicles', blank=True)
    # image = models.ImageField(upload_to='uploads/properties')
    images = models.ManyToManyField('PropertyImage', blank=True, related_name='properties')
    owner = models.ForeignKey(User,related_name='properties', on_delete=models.CASCADE)

    #status
    is_available = models.BooleanField(default=True)
    is_insured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.title}"
    
    def primary_image_url(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return f'{settings.WEBSITE_URL}{primary.image.url}'
        first = self.images.first()
        if first:
            return f'{settings.WEBSITE_URL}{first.image.url}'
        return None
    
class PropertyImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name='property_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/properties')
    is_primary = models.BooleanField(default=False, help_text="Main display image")
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',"Pending"),
        ('confirmed',"Confirmed"),
        ('active',"Active"),
        ('completed',"Completed"),
        ('cancelled',"Cancelled"),
        ('disputed',"Disputed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name='bookings',on_delete=models.CASCADE)

    # Dates
    start