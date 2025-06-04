from rest_framework import serializers
from .models import CustomUser, Conversation, Message
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(source='content')
    sent_at = serializers.DateTimeField(source='timestamp')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message_body', 'sent_at', 'is_read', 'attachment']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'is_group', 'participants', 'created_at', 'updated_at', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.order_by('-timestamp')[:10]  # Last 10 messages
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        if not data.get('participants'):
            raise ValidationError("A conversation must have at least one participant.")
        return data
