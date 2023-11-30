from rest_framework import generics, permissions, status
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password,check_password


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Update based on your authentication logic


    def perform_create(self, serializer):
        # Ensure the password is hashed before saving the user
        password = serializer.validated_data.get('password')
        print(f"Created Password: {password}")
        hashed_password = make_password(password)
        print(f"Hashed Password: {hashed_password}")
        serializer.save(password=hashed_password)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Update based on your authentication logic


class LoginAPIView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            print(f"User with email {username} not found.")
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        hashed_password = make_password(password)
        print(f"hashed password when login : {hashed_password}")
        print(f"User hashed password in database: {user.password}")
        if check_password(password, user.password):
            print(f"User hashed password in database: {user.password}")
            # login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            
            print(f"Invalid password for user with username {username}.")
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

