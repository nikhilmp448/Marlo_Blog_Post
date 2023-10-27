from rest_framework import serializers
from .models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email','firstname','lastname','password')
        extra_kwargs={'email':{'write_only':False,'required':True},'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account(
                email=validated_data['email'],
                firstname =validated_data['firstname'],
                lastname = validated_data['lastname']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user
