from rest_framework import serializers

from messaging.models import Message


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MessageSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'replies']
