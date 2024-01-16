from django.shortcuts import render
from users.models import User
from rest_framework import views,generics,status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from users.serializers import UserRegisterSerializer
from rest_framework.response import Response
import requests


class UserRegisterView(generics.CreateAPIView):
    # Define the queryset for the view, in this case, all User objects
    queryset = User.objects.all()

    # Specify the serializer class to be used for creating new users
    serializer_class = UserRegisterSerializer

    def get_serializer_context(self, *args, **kwargs):
        # Provide additional context to the serializer, such as request, args, and kwargs
        return {
            "request": self.request,
            "args": self.args,
            "kwargs": self.kwargs
        }

class UserLoginView(views.APIView):

    def post(self, request, *args, **kwargs):
        # Extract username and password from request data
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        # Check if username and password are provided
        if not username or not password:
            return Response({'success': False, 'data': {}, 'message': 'Provide username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = None

        # Check if username is numeric, then try to find user by mobile number, else by email
        if username.isnumeric():
            user = User.objects.filter(mobile=username).first()
        else:
            user = User.objects.filter(email__iexact=username).first()
        
        # If no user found, return invalid credentials response
        if not user:
            return Response({'success': False, 'data': {}, 'message': 'Invalid credentials! '}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if the provided password is correct
        if user.check_password(password):
            if user.is_active:
                # If user is active, generate an authentication token and return success response
                resp = {
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'mobile': user.mobile,
                    'email': user.email,
                    'active': user.is_active,
                    'auth_token': self.get_auth_token(user)
                }
                return Response({'success': True, 'data': resp, 'message': 'Successfully Logged In! '}, status=status.HTTP_200_OK)
            else:
                # If user is not active, return account deactivated response
                return Response({'success': False, 'data': {}, 'message': 'Account deactivated! Contant Admin.'}, status=status.HTTP_403_FORBIDDEN)
            
        # If password is incorrect, return invalid credentials response
        return Response({'success': False, 'data': {}, 'message': 'Invalid credentials! , Check username or password '}, status=status.HTTP_403_FORBIDDEN)
    

    def get_auth_token(self, user: User) -> dict:
        # Generate or retrieve an authentication token for the user
        token, created = Token.objects.get_or_create(user=user)
        token_response = {
            'token': str(token.key),
        }
        return token_response


class UserLogout(views.APIView):
    # Specify the permission classes required for this view, in this case, IsAuthenticated
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Call the Django `logout` function to log the user out
        logout(request)
        
        # Return a success response indicating successful logout
        return Response({"success": True, "message": "You have been successfully logged out"}, status=200)
    



class HistoricWeatherAPIView(views.APIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request,*args, **kwargs):
        data = request.data
        # Get latitude, longitude, and number of days from the request
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        num_days = data.get('num_days')


        # Validate input
        if not latitude or not longitude or not num_days:
            return Response({'error': 'Latitude, longitude, and num_days are required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            num_days = int(num_days)
        except ValueError:
            return Response({'error': 'Invalid data format for latitude, longitude, or num_days.'}, status=status.HTTP_400_BAD_REQUEST)


        # Make a request to Open Meteo API
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&past_days={num_days}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'


        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to fetch weather data from Open Meteo.'}, status=response.status_code)