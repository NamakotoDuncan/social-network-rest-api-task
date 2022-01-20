from rest_framework import serializers

from network.models import Post, CustomUser


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')
    author_id = serializers.IntegerField(source='author.id')
    date_modified = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'author', 'title', 'text', 'created_date', 'date_modified', 'likes')


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_id = serializers.SerializerMethodField()
    date_modified = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'author_id', 'author', 'title', 'text', 'created_date', 'date_modified')

    def get_author_id(self, obj):
        return self.context['request'].user.id


class PostUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_id = serializers.SerializerMethodField()
    date_modified = serializers.ReadOnlyField

    class Meta:
        model = Post
        fields = ('title', 'text', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'password')

        def create(self, validated_data):
            pass
            # prepare_and_submit_data.delay(request.data['email'])


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'joined_on_holiday', 'ip_address',
            'country', 'email_valid')
