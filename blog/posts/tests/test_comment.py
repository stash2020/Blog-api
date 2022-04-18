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

from posts.models import Post, Comment
from posts.serializers import CommentCreateUpdateSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class CommentListCreateAPIViewTestCase(APITestCase):
    
    def setUp(self):           
        self.username = "test"        
        self.password = "abcd1234"
        self.user = User.objects.create_user(username = self.username, password = self.password)
        self.user_2 = User.objects.create_user(username = "test2", password = self.password)
        self.post = Post.objects.create(title="test", body="this is test comment.")              
        
    def tearDown(self):
        self.user.delete()        
        self.user_2.delete()        
        self.post.delete()

    def test_unauthorized_user_cannot_create_comment(self):
        url = reverse("posts:create_comment", kwargs={"id": self.post.pk})        
        res = self.client.post(url, {"parent": self.post, "author": self.user_2, "body": "this is test comment."})        
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

    def test_create_comment(self):      
        url = reverse("posts:create_comment", kwargs={"id": self.post.pk})  
        self.client.force_login(self.user_2)
        res = self.client.post(url, { "body": "this is test comment."})            
        self.assertEqual(res.status_code, HTTP_201_CREATED)
    
    def test_comment_created_detail(self):        
        Comment.objects.create(parent = self.post, author = self.user_2, body="this is test comment.")
        url = reverse("posts:list_comment", kwargs={"id": self.post.pk})
        res = self.client.get(url)
        self.assertTrue(len(json.loads(res.content)) == Comment.objects.count())

class CommentDetailAPIViewTestCase(APITestCase):
    
    def setUp(self):
        self.username = "test"        
        self.password = "abcd1234"
        self.user = User.objects.create_user(username = self.username, password = self.password)
        self.user_2 = User.objects.create_user(username = "test2", password = self.password)
        self.user_3 = User.objects.create_user(username = "test3", password = self.password)
        self.post = Post.objects.create(title="test", body="this is test post.")      
        self.comment = Comment.objects.create(parent = self.post, author = self.user_2, body="this is test comment.")               
        self.url = reverse("posts:comment_detail", kwargs={"id": self.post.pk, "id_2": self.comment.pk})        

    def tearDown(self):
        self.user.delete()        
        self.user_2.delete()        
        self.user_3.delete()        
        self.post.delete()
        self.comment.delete()

    def test_post_object_bundle(self):        
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, HTTP_200_OK)

        comment_serializer_data = CommentCreateUpdateSerializer(instance=self.comment).data        
        res_data = json.loads(res.content)        
        self.assertEqual(comment_serializer_data, res_data)

    def test_comment_object_update_authorization(self):        
        self.client.force_login(self.user_3)
        # HTTP PUT
        res = self.client.put(self.url, {"body": "this is test comment."})
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

        # HTTP PATCH
        res = self.client.patch(self.url, {"body": "this is test comment."})
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

    def test_comment_put_object_update(self):        
        self.client.force_login(self.user_2)
        res = self.client.put(self.url, {"body": "this is NEW test comment."})
        res_data = json.loads(res.content)
        comment = Comment.objects.get(id=self.comment.id)
                
        self.assertEqual(res_data.get("body"), comment.body)

    def test_comment_object_delete(self):
        self.client.force_login(self.user_2)
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_other_user_comment(self):
        self.client.force_login(self.user_3)
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)
