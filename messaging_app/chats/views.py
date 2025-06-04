from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        # Optional: accept other participants via POST data
        participant_ids = self.request.data.get("participant_ids", [])
        for user_id in participant_ids:
            try:
                user = CustomUser.objects.get(id=user_id)
                conversation.participants.add(user)
            except CustomUser.DoesNotExist:
                continue
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.kwargs['conversation_pk']).select_related('sender', 'conversation')

    def perform_create(self, serializer):
        conversation = get_object_or_404(Conversation, pk=self.kwargs['conversation_pk'])
        serializer.save(sender=self.request.user, conversation=conversation)

