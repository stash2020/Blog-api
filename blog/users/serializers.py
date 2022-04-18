from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password":{
            "write_only": True,
            "style": {"input_type": "password"}
        }}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        user_obj = User(username=username)
        user_obj.set_password(password) # password hashed before stored
        user_obj.save()
        return user_obj