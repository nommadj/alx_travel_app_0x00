from rest_framework import serializers

class DummySerializer(serializers.Serializer):
    message = serializers.CharField()
