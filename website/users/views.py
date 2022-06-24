from rest_framework.views import APIView
from users.serializers import UsersDetailSerializer
from users.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status


class UsersDetailView(APIView):
    def get(self, request, pk):
        if request.user.id != pk:
            return Response({"status": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, pk=pk)
        serializer = UsersDetailSerializer(user)
        return Response(serializer.data)
