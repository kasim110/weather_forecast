from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    # SerializerMethodField for a custom message
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        # Define the model and fields for the serializer
        model = User
        fields = [
            'first_name', 'last_name', 'mobile', 'email', 'password', 'message'
        ]

        # Specify additional kwargs for fields, e.g., making the password write-only
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        # Custom method to provide a message for the registration response
        return "Thank you for registering. Please verify your Email Id before continuing."
    
    def validate_mobile(self, value):
        # Custom validation for mobile number uniqueness
        qs = User.objects.filter(email=value)

        if qs.exists():
            raise serializers.ValidationError("User with this Email Id  already registered.")
        return value
    
    def create(self, validated_data):
        # Custom create method to create a new user
        # Utilizes a custom manager method create_new_user to handle user creation
        user_obj = User.objects.create_new_user(**validated_data, is_active=True)

        return user_obj
