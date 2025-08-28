from rest_framework import serializers

from project_apps.chats.models import ConversationItem, ConversationThread


class MessageSerializer(serializers.Serializer):
    """Serializer for chat messages in the NOA API."""

    role = serializers.CharField()
    content = serializers.CharField()


class MultimodalRequestSerializer(serializers.Serializer):
    """Serializer for the NOA multimodal request."""

    messages = MessageSerializer(many=True, required=False)
    prompt = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    gps = serializers.ListField(child=serializers.FloatField(), required=False)
    local_time = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    vision = serializers.CharField(required=False)
    assistant = serializers.CharField(required=False)
    assistant_model = serializers.CharField(required=False)

    # Additional fields can be added as needed


class TokenUsageSerializer(serializers.Serializer):
    """Serializer for token usage by model."""

    input_tokens = serializers.IntegerField()
    output_tokens = serializers.IntegerField()
    total_tokens = serializers.IntegerField(required=False)  # Optional field


class MultimodalResponseSerializer(serializers.Serializer):
    """Serializer for the NOA multimodal response."""

    user_prompt = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    debug = serializers.DictField(required=True)
    image = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    token_usage_by_model = serializers.DictField(
        child=TokenUsageSerializer(),
        required=False,
    )
    capabilities_used = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    total_tokens = serializers.IntegerField(required=False, allow_null=True)
    input_tokens = serializers.IntegerField(required=False, allow_null=True)
    output_tokens = serializers.IntegerField(required=False, allow_null=True)
    timings = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class ConversationThreadSerializer(serializers.ModelSerializer):
    """Serializer for ConversationThread model."""

    class Meta:
        model = ConversationThread
        fields = ["id", "name", "type", "created_at"]


class ConversationItemSerializer(serializers.ModelSerializer):
    """Serializer for ConversationItem model."""

    class Meta:
        model = ConversationItem
        fields = ["id", "prompt", "response", "tokens", "created_at"]
