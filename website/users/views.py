from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UsersDetailSerializer


class UsersDetailView(APIView):
    """
    Returns a user with a certain pk if it's equal to the currently logged in one.
    """

    def get(self, request, pk):
        if request.user.id != pk:
            return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        serializer = UsersDetailSerializer(user)
        return Response(serializer.data)
