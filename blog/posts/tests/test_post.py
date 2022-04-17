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

from posts.models import Post
from posts.serializers import PostDetailSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class PostListCreateAPIViewTestCase(APITestCase):
    
    def setUp(self):           
        self.username = 'test'        
        self.password = 'abcd1234'
        self.user = User.objects.create(username = self.username)
        self.user.set_password(self.password)
        self.user.save()
        
    def tearDown(self):
        self.user.delete()        

    def test_unauthorized_user_cannot_create_post(self):
        url = reverse('posts:create_post')
        res = self.client.post(url, {'title': 'test', 'body': 'this is test post.'})
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

    def test_create_post(self):        
        url = reverse('posts:create_post')
        self.client.force_login(self.user)
        res = self.client.post(url, {'title': 'test', 'body': 'this is test post.'})               
        self.assertEqual(res.status_code, HTTP_201_CREATED)
    
    def test_post_created_detail(self):        
        Post.objects.create(title='test', body='this is test post.')
        url = reverse('posts:list_post')
        res = self.client.get(url)

        self.assertTrue(len(json.loads(res.content)) == Post.objects.count())

class PostDetailAPIViewTestCase(APITestCase):
    
    def setUp(self):
        self.username = 'test'        
        self.password = 'abcd1234'
        self.user = User.objects.create(username = self.username)
        self.user.set_password(self.password)     
        self.user.save()   
        self.post = Post.objects.create(title='test', body='this is test post.')               
        self.url = reverse('posts:post_detail', kwargs={'id': self.post.pk})        

    
    def test_post_object_bundle(self):        
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, HTTP_200_OK)

        post_serializer_data = PostDetailSerializer(instance=self.post).data        
        res_data = json.loads(res.content)        
        self.assertEqual(post_serializer_data, res_data)

    def test_post_object_update_authorization(self):        
        new_user = User.objects.create_user(username = 'newuser', password = 'newpass')
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        # HTTP PUT
        res = self.client.put(self.url, {'title': 'test', 'body': 'this is test post.'})
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

        # HTTP PATCH
        res = self.client.patch(self.url, {'title': 'test', 'body': 'this is test post.'})
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

    def test_post_put_object_update(self):        
        self.client.force_login(self.user)
        res = self.client.put(self.url, {'title': 'new test', 'body': 'this is NEW test post.'})
        res_data = json.loads(res.content)
        post = Post.objects.get(id=self.post.id)
        
        self.assertEqual(res_data.get('title'), post.title)
        self.assertEqual(res_data.get('body'), post.body)

    def test_post_object_delete(self):
        self.client.force_login(self.user)
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, HTTP_204_NO_CONTENT)