from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword"
        }
        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_update(self):
        data = {"bio": "Updated bio"}
        response = self.client.patch(f'/api/v1/users/{self.user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], "Updated bio")

    def test_user_delete(self):
        response = self.client.delete(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostAPITests(APITestCase):

    def setUp(self):
        # Create test user and post
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.post = Post.objects.create(user=self.user, content="Test post")

    def test_create_post(self):
        data = {"content": "New post content"}
        response = self.client.post('/api/v1/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], "New post content")

    def test_get_all_posts(self):
        response = self.client.get('/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_own_post(self):
        data = {"content": "Updated post content"}
        response = self.client.patch(f'/api/v1/posts/{self.post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "Updated post content")

    def test_delete_own_post(self):
        response = self.client.delete(f'/api/v1/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentAPITests(APITestCase):

    def setUp(self):
        # Create test user, post, and comment
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.post = Post.objects.create(user=self.user, content="Test post")
        self.comment = Comment.objects.create(user=self.user, post=self.post, content="Test comment")

    def test_create_comment(self):
        data = {"post": self.post.id, "content": "New comment content"}
        response = self.client.post('/api/v1/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], "New comment content")

    def test_get_all_comments(self):
        response = self.client.get('/api/v1/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_own_comment(self):
        data = {"content": "Updated comment content"}
        response = self.client.patch(f'/api/v1/comments/{self.comment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "Updated comment content")

    def test_delete_own_comment(self):
        response = self.client.delete(f'/api/v1/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LikeAPITests(APITestCase):

    def setUp(self):
        # Create test user and post
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.post = Post.objects.create(user=self.user, content="Test post")

    def test_like_post(self):
        data = {"post": self.post.id}
        response = self.client.post('/api/v1/likes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_likes(self):
        Like.objects.create(user=self.user, post=self.post)
        response = self.client.get('/api/v1/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unlike_post(self):
        like = Like.objects.create(user=self.user, post=self.post)
        response = self.client.delete(f'/api/v1/likes/{like.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)