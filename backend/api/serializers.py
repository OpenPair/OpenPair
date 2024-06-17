from rest_framework import serializers
from .models import LatestCount, Vocab

class CurrentCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = LatestCount
        fields = ['id', 'current_count', 'author']
        extra_kwargs = {'author': {'read_only': True}}

class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        fields = ['id', 'word', 'definition']

# ? Attempting to serialize the OpenAi response object
class TextSerializer(serializers.Serializer):
    value = serializers.CharField()
    annotations = serializers.ListField(child=serializers.CharField(), required=False)

class ContentSerializer(serializers.Serializer):
    type = serializers.CharField()
    text = TextSerializer()

class MessageSerializer(serializers.Serializer):
    id = serializers.CharField()
    object = serializers.CharField()
    created_at = serializers.IntegerField()
    assistant_id = serializers.CharField()
    thread_id = serializers.CharField()
    run_id = serializers.CharField()
    role = serializers.CharField()
    content = ContentSerializer(many=True)
    attachments = serializers.ListField(required=False)
    metadata = serializers.DictField(required=False)
    vocab = VocabSerializer(many=True, required=False)
