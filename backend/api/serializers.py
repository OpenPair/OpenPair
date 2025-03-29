from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    id = serializers.CharField()
    role = serializers.CharField()
    content = serializers.CharField()  # Always expect a simple string content
    timestamp = serializers.IntegerField()  # Unix timestamp for message creation time
