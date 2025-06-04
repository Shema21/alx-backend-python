from rest_framework import viewsets, permissions, filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'participants__username']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
