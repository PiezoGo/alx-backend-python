from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        participant_ids = request.data.get('participants', [])

        if not participant_ids:
            return Response(
                {"error": "At least one participant is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch users
        participants = User.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            return Response(
                {"error": "Invalid participant IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """Send a message to an existing conversation."""
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        sender_id = request.data.get('sender')

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation, sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, pk=conversation_id)
        sender = get_object_or_404(User, pk=sender_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
