from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    """
    Represents a listing available for booking.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    max_guests = models.IntegerField()
    amenities = models.TextField(blank=True, null=True, help_text="Comma separated list of amenities")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    """
    Represents a booking made by a user for a listing.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_guests = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('listing', 'check_in_date', 'check_out_date', 'user')

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.user.username}"

class Review(models.Model):
    """
    Represents a review given by a user for a listing they booked.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('listing', 'user')

    def __str__(self):
        return f"Review for {self.listing.title} by {self.user.username} - Rating: {self.rating}"
