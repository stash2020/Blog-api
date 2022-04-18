import json

from rest_framework.status import \
    HTTP_200_OK, \
    HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST    

from django.urls import reverse
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationAPIViewTestCase(APITestCase):

    def setUp(self):   
        self.register_url = reverse("users:user_create")
        self.login_url = reverse("api-auth:login")
        
        self.user_data = {
            "username" : "test",
            "password" : "abcd1234"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_user_cannot_register_with_no_data(self):        
        res = self.client.post(self.register_url)        
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")          
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual(res.data["username"], self.user_data["username"])
   
    def test_registration_of_unique_user(self):
        user = User.objects.create(username = self.user_data["username"])
        user.set_password(self.user_data["password"])
        user.save()
        res = self.client.post(self.register_url, self.user_data, format="json")          
        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)



class UserLoginAPIViewTestCase(APITestCase):
    
    def setUp(self):   
        self.register_url = reverse("users:user_create")
        self.login_url = reverse("api-auth:login")
        
        self.username = "test"        
        self.password = "abcd1234"
        self.user = User.objects.create(username = self.username)
        self.user.set_password(self.password)
        self.user.save()
        
    def tearDown(self):
        self.user.delete()        
    
    def test_authentication_without_password(self):                
        res = self.client.login(username = self.username)        
        self.assertEqual(res, False)
    
    def test_authentication_with_wrong_password(self):
        res = self.client.login(username = self.username, password = "wrong")        
        self.assertEqual(res, False)
    
    # check it later
    #def test_authentication_with_valid_data(self):
    #    res = self.client.post(self.login_url, username = self.username, password = self.password)                      
    #    self.assertEqual(res.status_code, HTTP_200_OK)
    #    self.assertTrue("token" in json.loads(res.content))

    def test_user_can_login(self):        
        res = self.client.post(self.login_url, {"username": self.username, "password": self.password}, format="json")        
        self.assertEqual(res.status_code, HTTP_200_OK)
        