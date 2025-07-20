from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample data for listings.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        # Clear existing data to prevent duplicates on successive runs
        Booking.objects.all().delete() # Delete bookings first due to foreign key constraint
        Review.objects.all().delete() # Delete reviews first due to foreign key constraint
        Listing.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing Listing, Booking, and Review data.'))

        # Create a superuser if one doesn't exist (for associating bookings/reviews)
        if not User.objects.filter(username='seeder_user').exists():
            user = User.objects.create_user(
                username='seeder_user',
                email='seeder@example.com',
                password='seederpassword123'
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
        else:
            user = User.objects.get(username='seeder_user')
            self.stdout.write(self.style.SUCCESS(f'Using existing user: {user.username}'))

        # Sample data for listings
        listings_data = [
            {
                'title': 'Cozy Apartment in City Center',
                'description': 'A charming and comfortable apartment right in the heart of the city, perfect for tourists and business travelers.',
                'price_per_night': 85.00,
                'address': '123 Main St',
                'city': 'Nairobi',
                'country': 'Kenya',
                'image_url': 'https://example.com/images/nairobi_apt1.jpg',
                'max_guests': 4,
                'amenities': 'WiFi, Kitchen, AC, TV'
            },
            {
                'title': 'Spacious Villa with Ocean View',
                'description': 'Enjoy breathtaking ocean views from this luxurious and spacious villa. Ideal for family vacations.',
                'price_per_night': 350.00,
                'address': '456 Ocean Dr',
                'city': 'Mombasa',
                'country': 'Kenya',
                'image_url': 'https://example.com/images/mombasa_villa1.jpg',
                'max_guests': 8,
                'amenities': 'Pool, Beach Access, WiFi, BBQ'
            },
            {
                'title': 'Rustic Cabin in the Forest',
                'description': 'Escape to nature in this peaceful and rustic cabin. Perfect for a quiet getaway.',
                'price_per_night': 60.00,
                'address': '789 Forest Rd',
                'city': 'Naivasha',
                'country': 'Kenya',
                'image_url': 'https://example.com/images/naivasha_cabin1.jpg',
                'max_guests': 2,
                'amenities': 'Fireplace, Hiking Trails'
            },
            {
                'title': 'Modern Loft in Tech Hub',
                'description': 'Stylish loft apartment in a vibrant tech district. Close to co-working spaces and cafes.',
                'price_per_night': 120.00,
                'address': '101 Innovation Blvd',
                'city': 'Nairobi',
                'country': 'Kenya',
                'image_url': 'https://example.com/images/nairobi_loft1.jpg',
                'max_guests': 3,
                'amenities': 'High-speed WiFi, Workspace, Gym Access'
            },
            {
                'title': 'Safari Tent in Maasai Mara',
                'description': 'Experience the wild with a comfortable stay in a luxury safari tent. Daily game drives included.',
                'price_per_night': 500.00,
                'address': 'Maasai Mara Reserve',
                'city': 'Narok',
                'country': 'Kenya',
                'image_url': 'https://example.com/images/mara_tent1.jpg',
                'max_guests': 2,
                'amenities': 'Game Drives, All-Inclusive Meals'
            }
        ]

        # Create Listing objects
        for data in listings_data:
            listing = Listing.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created listing: "{listing.title}"'))

            # Optionally, create some sample bookings and reviews for each listing
            if random.random() < 0.7:  # 70% chance to add a booking
                check_in = date.today() + timedelta(days=random.randint(7, 30))
                check_out = check_in + timedelta(days=random.randint(2, 7))
                total_price = listing.price_per_night * (check_out - check_in).days
                booking = Booking.objects.create(
                    listing=listing,
                    user=user,
                    check_in_date=check_in,
                    check_out_date=check_out,
                    total_price=total_price,
                    number_of_guests=random.randint(1, listing.max_guests)
                )
                self.stdout.write(self.style.SUCCESS(f'  - Created booking for "{listing.title}"'))

            if random.random() < 0.6:  # 60% chance to add a review
                review = Review.objects.create(
                    listing=listing,
                    user=user,
                    rating=random.randint(3, 5),
                    comment=random.choice([
                        "Absolutely fantastic stay! Highly recommend.",
                        "Great place, clean and well-located.",
                        "Had a wonderful time, very comfortable.",
                        "Good value for money, but a bit noisy.",
                        "Excellent host and beautiful property."
                    ])
                )
                self.stdout.write(self.style.SUCCESS(f'  - Created review for "{listing.title}" (Rating: {review.rating})'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
