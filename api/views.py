import jwt
import datetime
from django.contrib.auth import user_logged_in
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler

from network.tasks import prepare_and_submit_data
from . import serializers
from network.models import Post, CustomUser, PostLikes
from social import settings

import logging

from .serializers import PostUpdateSerializer

logger = logging.getLogger(__name__)


class ApiStatus(APIView):
    def get(self, request):
        response = Response()
        response.data = {
            'message': 'Social API Up and Running',
        }

        return response


class PostList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        post_obj = Post.objects.all()
        serializer = serializers.PostSerializer(post_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        post_obj = get_object_or_404(Post, pk=pk)
        serializer = serializers.PostSerializer(post_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = serializers.PostCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostLike(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        user = self.request.user
        response = {}

        if post:
            response['message'] = 'You successfully liked the post'

            like = PostLikes.objects.filter(post_id=post, user_id=user).first()
            if like:
                if like.type == 1:
                    like.type = 0
                    post.likes = post.likes - 1
                    response['message'] = 'You successfully unliked the post'
                elif like.type == 0:
                    like.type = 1
                    post.likes = post.likes + 1

                like.date = timezone.now()
            else:
                like = PostLikes(post_id=post, user_id=user, type=1)
                post.likes = post.likes + 1

            post.save()
            like.save()

            return Response(response, status=status.HTTP_200_OK)
        else:
            response['message'] = f'Post with ID {pk} not found'
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class PostUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        post_serializer = PostUpdateSerializer(instance=post, data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response(post_serializer.data, status=status.HTTP_200_OK)


class PostDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUser(APIView):
    def post(self, request):
        user = request.data
        ip_address = self.request.META["REMOTE_ADDR"]
        user['ip_address'] = ip_address
        serializer = serializers.UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        prepare_and_submit_data.delay(request.data['email'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthenticateUser(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.get(email=email, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            user_details = {'name': "%s %s" % (
                user.first_name, user.last_name), 'token': token}
            user_logged_in.send(sender=user.__class__,
                                request=request, user=user)
            return Response(user_details, status=status.HTTP_200_OK)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = serializers.UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
