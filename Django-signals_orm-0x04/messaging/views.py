from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from messaging.models import Message
from messaging.serializers import MessageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages(request):
    messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@cache_page(60)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_api(request):
    receiver_id = request.GET.get('receiver')
    if not receiver_id:
        return Response({"error": "Receiver not specified."}, status=400)

    messages = Message.objects.filter(
        sender=request.user,
        receiver__id=receiver_id,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'message': 'Your account and all related data have been deleted.'})
