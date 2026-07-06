from django.contrib import admin

# Register your models here.
from .models import Property, PropertyImage

# Replaced the below because it doesnt allow for admin to show image attribute directly
# admin.site.register(Property)

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 2
    fields = ['image', 'is_primary', 'caption']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'make', 'model', 'year', 'price_per_day', 'is_available', 'created_at']
    inlines = [PropertyImageInline]
    fields = [
        'title', 'description', 'price_per_day',
        'make', 'model', 'year', 'license_plate',
        'color', 'seats', 'transmission', 'fuel_type',
        'country', 'country_code', 'city', 'address', 'category',
        'favorited', 'owner', 'is_available', 'is_insured',
    ]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property_listing', 'caption', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']