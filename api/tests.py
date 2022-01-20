import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import Post, CustomUser


class UserModelTest(TestCase):
    def setup(self):
        CustomUser.objects.create(username='usernametest', email='Casper@gmail.com', first_name='fn', last_name='ln',
                                  password='Secr3ts')

    def test_user_fields(self):
        user = Post.CustomUser.get(email='Casper@gmail.com')
        self.assertEqual(user.title, "model test")
        self.assertIsNot(user.email, "3")


class UserApiTests(APITestCase):
    def setUp(self):
        self.data = {
            "id": 5,
            "username": "newuser-api",
            "email": "newapiuser@gmail.com",
            "first_name": "New User4",
            "last_name": "New User4",
            "date_joined": "2022-01-08T17:19:20.747820Z",
            "password": "1234563",
            'ip_address': '35.51.29.44'
        }
        self.response = self.client.post('/api/signup', json.dumps(self.data), content_type='application/json')

    def test_api_create_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'newuser-api')

    def test_api_user_login(self):
        user = CustomUser.objects.get()
        payload = {'email': user.email, 'password': user.password}
        response = self.client.post('/api/login', json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_20O_OK)

    def test_api_get_user_infor(self):
        user = CustomUser.objects.get()
        response = self.client.get('/api/user/{0}'.format(user.id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_20O_OK)


class PostModelTests(TestCase):
    def setUp(self):
        Post.objects.create(author_id=1, author='Casper', title='model test', text='model test text')

    def test_post_fields(self):
        casper = Post.objects.get(author_id=1)
        self.assertEqual(casper.title, "model test")
        self.assertIsNot(casper.author_id, "3")


class PostApiTests(APITestCase):
    def setUp(self):
        self.data = {
            "author_id": 1,
            "title": "Post text API",
            "text": "Yes, it'\''s really work!",
            "created_date": "2021-10-23T19:21:41.969850Z",
            "date_modified": "23 Oct 2021",
            "likes": 0
        }
        self.response = self.client.post('/api/post-create', json.dumps(self.data), content_type='application/json')

    def test_api_create_post(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Post text API')

    def test_api_get_posts(self):
        url = '/api/post'
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1)

    def test_api_get_post(self):
        url = '/api/post/{0}'
        post = Post.objects.get()
        response = self.client.get(url.format(post.id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, post)

    def test_api_like_post(self):
        url = '/api/post/{0}/like'
        post = Post.objects.get()
        response = self.client.post(url.format(post.id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_unlike_post(self):
        url = '/api/post/{0}/like'
        post = Post.objects.get()
        response = self.client.post(url.format(post.id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_update_post(self):
        post = Post.objects.get()
        new_data = {
            "title": "UpdatesPost text API",
            "text": "Yes, updates really work!",
        }
        url = '/api/post/{0}'
        response = self.client.put(url.format(post.id), data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get().title, 'UpdatesPost text API')

    def test_api_delete_post(self):
        post = Post.objects.get()
        url = '/api/post/{0}'
        response = self.client.delete(url.format(post.id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 0)
