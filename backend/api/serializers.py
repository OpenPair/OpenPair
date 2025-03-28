from rest_framework import serializers
from .models import LatestCount, Vocab

class CurrentCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = LatestCount
        fields = ['id', 'current_count', 'author']
        extra_kwargs = {'author': {'read_only': True}}

# class VocabSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vocab
#         fields = ['id', 'word', 'definition']

# ? Attempting to serialize the OpenAi response object
class TextSerializer(serializers.Serializer):
    value = serializers.CharField()
    annotations = serializers.ListField(child=serializers.CharField(), required=False)

class ContentSerializer(serializers.Serializer):
    # This definitely makes no sense
    def to_representation(self, instance):
        # If instance is a string, return it directly
        if isinstance(instance, str):
            return instance
        # Otherwise, handle the nested structure
        return super().to_representation(instance)
    
    text = TextSerializer(required=False)  # Make text field optional

class MessageSerializer(serializers.Serializer):
    id = serializers.CharField()
    role = serializers.CharField()
    content = serializers.CharField()  # Always expect a simple string content
    created_at = serializers.IntegerField()  # Unix timestamp for message creation time
