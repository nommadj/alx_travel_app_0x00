from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth.models import User

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    Includes read-only fields for related bookings and reviews count.
    """
    bookings_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price_per_night', 'address', 'city', 'country',
            'image_url', 'max_guests', 'amenities', 'created_at', 'updated_at',
            'bookings_count', 'reviews_count', 'average_rating'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_bookings_count(self, obj):
        return obj.bookings.count()

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(average_rating=serializers.Avg('rating'))['average_rating']


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    Includes read-only fields for listing title and username.
    """
    listing_title = serializers.ReadOnlyField(source='listing.title')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'user', 'username', 'check_in_date',
            'check_out_date', 'total_price', 'number_of_guests', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_price']

    def validate(self, data):
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    Includes read-only field for username.
    """
    username = serializers.ReadOnlyField(source='user.username')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = Review
        fields = [
            'id', 'listing', 'listing_title', 'user', 'username', 'rating', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
