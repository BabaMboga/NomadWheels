import uuid
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

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
    # images = models.ManyToManyField('PropertyImage', blank=True, related_name='properties')
    owner = models.ForeignKey(User,related_name='properties', on_delete=models.CASCADE)

    #status
    is_available = models.BooleanField(default=True)
    is_insured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.title}"
    
    @property
    def primary_image_url(self):
        primary = self.images.filter(is_primary=True).first()
        img = primary or self.images.first()
        if img and img.image:
            website_url = getattr(settings,'WEBSITE_URL', '')
            return f'{website_url}{img.image.url}'
        return None
        # if primary:
        #     return f'{settings.WEBSITE_URL}{primary.image.url}'
        # first = self.images.first()
        # if first:
        #     return f'{settings.WEBSITE_URL}{first.image.url}'
        # return None
    
class PropertyImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_listing = models.ForeignKey(
        Property, 
        related_name='images', 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='uploads/properties')
    is_primary = models.BooleanField(default=False, help_text="Main display image")
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        return f"{settings.WEBSITE_URL}{self.image.url}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            PropertyImage.objects.filter(
                property=self.property_listing,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)

            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.caption or self.image.name or "Unnamed Image"
    
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
    start_date = models.DateField(help_text="Pickup date")
    end_date = models.DateField(help_text="Return date")
    pickup_time = models.TimeField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)

    # Duration & pricing
    number_of_days = models.IntegerField()
    daily_rate = models.IntegerField(help_text="Rate applied at time of booking")
    total_price = models.FloatField()

    # Drive details
    primary_driver = models.ForeignKey(
        User,
        related_name = 'bookings',
        on_delete=models.CASCADE,
        help_text="The user who made the booking"
    )
    additional_drivers = models.ManyToManyField(
        User,
        related_name='additional_drivers',
        blank=True,
        help_text="A second driver allowed to handle the property"
    )

    # requirements
    driver_age = models.IntegerField(null=True, blank=True)
    has_valid_license = models.BooleanField(default=False)
    license_number = models.CharField(max_length=100, blank=True)
    license_expiry = models.DateField(null=True, blank=True)

    # Status & tracking 
    status = models.CharField(
        max_length=20,
        choices = STATUS_CHOICES,
        default='pending'
    )
    mileage_at_pickup = models.IntegerField(null=True, blank=True, help_text="Odometer reading")

    # Reviews
    owner_review = models.TextField(blank=True)
    renter_review = models.TextField(blank=True)

    class Rating(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"
    owner_rating = models.IntegerField(null=True, blank=True, choices=Rating.choices)
    renter_rating = models.IntegerField(null=True, blank=True, choices=Rating.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Booking #{str(self.id)[:8]} - {self.property}"