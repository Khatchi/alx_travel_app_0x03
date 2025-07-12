from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Booking

@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Send booking confirmation email to guest and host.
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        
        # Email to guest
        guest_subject = f'Booking Confirmation - {booking.listing.title}'
        guest_message = render_to_string('emails/booking_confirmation_guest.html', {
            'booking': booking,
            'guest_name': booking.guest.get_full_name() or booking.guest.username,
        })
        
        send_mail(
            subject=guest_subject,
            message=guest_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.guest.email],
            fail_silently=False,
            html_message=guest_message
        )
        
        # Email to host
        host_subject = f'New Booking Received - {booking.listing.title}'
        host_message = render_to_string('emails/booking_confirmation_host.html', {
            'booking': booking,
            'host_name': booking.listing.host.get_full_name() or booking.listing.host.username,
        })
        
        send_mail(
            subject=host_subject,
            message=host_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.listing.host.email],
            fail_silently=False,
            html_message=host_message
        )
        
        return f"Booking confirmation emails sent for booking {booking_id}"
        
    except Booking.DoesNotExist:
        return f"Booking {booking_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"