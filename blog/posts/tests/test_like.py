import json

from urllib import response
from rest_framework.status import \
    HTTP_200_OK, \
    HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT, \
    HTTP_400_BAD_REQUEST, \
    HTTP_403_FORBIDDEN

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from posts.models import Post, Like
from posts.serializers import LikeCreateUpdateSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class LikeListCreateAPIViewTestCase(APITestCase):
    
    def setUp(self):           
        self.username = 'test'        
        self.password = 'abcd1234'
        self.user = User.objects.create_user(username = self.username, password = self.password)
        self.post = Post.objects.create(title='test', body='this is test like.')      
        self.user_2 = User.objects.create_user(username = 'test2', password = self.password)
        
    def tearDown(self):
        self.user.delete()        
        self.user_2.delete()        
        self.post.delete()        

    def test_unauthorized_user_cannot_create_like(self):
        url = reverse('posts:create_like', kwargs={'id': self.post.pk})        
        res = self.client.post(url)        
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

    def test_create_like(self):      
        url = reverse('posts:create_like', kwargs={'id': self.post.pk})  
        self.client.force_login(self.user_2)
        res = self.client.post(url)            
        self.assertEqual(res.status_code, HTTP_201_CREATED)
    
    def test_like_created_detail(self):        
        Like.objects.create(parent = self.post, author = self.user_2)
        url = reverse('posts:list_like', kwargs={'id': self.post.pk})
        res = self.client.get(url)
        self.assertTrue(len(json.loads(res.content)) == Like.objects.count())

class LikeDetailAPIViewTestCase(APITestCase):
    
    def setUp(self):
        self.username = 'test'        
        self.password = 'abcd1234'
        self.user = User.objects.create_user(username = self.username, password = self.password)
        self.post = Post.objects.create(title='test', body='this is test post.')      
        self.user_2 = User.objects.create_user(username = 'test2', password = self.password)
        self.like = Like.objects.create(parent = self.post, author = self.user_2)               
        self.url = reverse('posts:like_detail', kwargs={'id': self.post.pk, 'id_2': self.like.pk})        

    
    def test_post_object_bundle(self):        
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, HTTP_200_OK)

        like_serializer_data = LikeCreateUpdateSerializer(instance=self.like).data        
        res_data = json.loads(res.content)               
        self.assertEqual(like_serializer_data, res_data)

    def test_like_object_delete(self):
        self.client.force_login(self.user_2)
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, HTTP_204_NO_CONTENT)

