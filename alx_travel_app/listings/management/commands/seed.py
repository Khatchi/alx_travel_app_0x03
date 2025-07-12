from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
import random

try:
    from faker import Faker
except ImportError:
    raise ImportError("Please install the 'Faker' library using pip: pip install Faker")

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with sample listings and users'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')
        self.create_users()
        listings_created = self.create_listings()
        self.stdout.write(self.style.SUCCESS(f'✅ Successfully seeded {listings_created} listings!'))

    def create_users(self):
        if not User.objects.filter(username='host1').exists():
            User.objects.create_user(
                username='host1',
                email='host1@example.com',
                password='testpass123',
                first_name='John',
                last_name='Doe'
            )
            self.stdout.write('👤 Created user: host1')

        if not User.objects.filter(username='guest1').exists():
            User.objects.create_user(
                username='guest1',
                email='guest1@example.com',
                password='testpass123',
                first_name='Jane',
                last_name='Smith'
            )
            self.stdout.write('👤 Created user: guest1')

    def create_listings(self):
        if Listing.objects.exists():
            self.stdout.write('⚠️ Listings already exist. Skipping creation.')
            return 0

        property_types = ['AP', 'HO', 'VI', 'CO', 'CA']
        amenities = ['WiFi', 'Pool', 'Kitchen', 'Parking', 'Air Conditioning', 'TV', 'Washer']
        host = User.objects.get(username='host1')

        for _ in range(10):
            selected_amenities = random.sample(amenities, random.randint(2, 5))
            Listing.objects.create(
                host=host,
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=5),
                address=fake.address(),
                property_type=random.choice(property_types),
                price_per_night=random.randint(50, 500),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                max_guests=random.randint(1, 10),
                amenities=selected_amenities
            )
        return 10
