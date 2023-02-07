from django.db import models
from commons.models import Common


class ChattingRoom(Common):
    """Chatting Room"""

    users = models.ManyToManyField(
        "users.user",
    )

    def __str__(self) -> str:
        return "Chat room"


class Message(Common):
    """Message model definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.user",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    chatroom = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
