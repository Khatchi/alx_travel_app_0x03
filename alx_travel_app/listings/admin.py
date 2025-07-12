from django.contrib import admin
from listings.models import Listing, Review, Booking

# Register your models here.

admin.site.register(Listing)
admin.site.register(Review)
admin.site.register(Booking)

