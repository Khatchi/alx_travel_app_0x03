from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['host', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['guest', 'total_price', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['booking', 'created_at']
        
