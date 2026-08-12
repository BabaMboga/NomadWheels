from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import uuid

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate_email(self, email):
        if get_adapter().is_email_taken(email):
            raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        validate_password(data['password1'], self.instance)
        return data

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        # auto-generaate a unique username since the field is required on the model
        user.username = f"user_{uuid.uuid4().hex[:12]}"

        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))
        adapter.save_user(request, user, self, commit=False)
        user.save()
        setup_user_email(request, user, [])
        
        return user