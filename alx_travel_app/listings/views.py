from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing listings. Only authenticated users can access.
    Hosts can create, update, and delete their own listings.
    """
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()

    def perform_create(self, serializer):
        """Ensure only authenticated users can create listings, setting themselves as host."""
        serializer.save(host=self.request.user)

    def perform_update(self, serializer):
        """Ensure only the host can update their listing."""
        if self.get_object().host != self.request.user:
            raise PermissionDenied("You can only update your own listings.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the host can delete their listing."""
        if instance.host != self.request.user:
            raise PermissionDenied("You can only delete your own listings.")
        instance.delete()

    @swagger_auto_schema(
        operation_description="List all listings or create a new listing.",
        responses={200: ListingSerializer(many=True), 201: ListingSerializer()}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings. Only authenticated users can access.
    Guests can create and view their bookings; hosts can view bookings for their listings.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()

    def get_queryset(self):
        """
        Return bookings for the authenticated user (guest) or their listings (host).
        """
        user = self.request.user
        return Booking.objects.filter(
            guest=user
        ) | Booking.objects.filter(
            listing__host=user
        )

    def perform_create(self, serializer):
        """Ensure only authenticated users can create bookings, setting themselves as guest."""
        listing = serializer.validated_data['listing']
        if not listing.is_active:
            raise PermissionDenied("This listing is not active.")
        serializer.save(guest=self.request.user, total_price=self.calculate_total_price(listing))

    def perform_update(self, serializer):
        """Ensure only the guest can update their booking."""
        booking = self.get_object()
        if booking.guest != self.request.user:
            raise PermissionDenied("You can only update your own bookings.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the guest can cancel their booking."""
        if instance.guest != self.request.user:
            raise PermissionDenied("You can only cancel your own bookings.")
        instance.status = 'CA'
        instance.save()

    def calculate_total_price(self, listing):
        """Calculate total price based on booking duration and listing price."""
        start_date = self.request.data.get('start_date')
        end_date = self.request.data.get('end_date')
        if start_date and end_date:
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            nights = (end - start).days
            return nights * listing.price_per_night
        return 0

    @swagger_auto_schema(
        operation_description="List all bookings for the user or create a new booking.",
        responses={200: BookingSerializer(many=True), 201: BookingSerializer()}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
