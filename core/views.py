from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.conf import settings
from .models import User
from .serializers import UserCreateSerialiser

# Create your views here.
@api_view(['POST'])
def google_register_view(request):
    try:
        auth_token = request.POST.get("google_acc")
        idinfo = id_token.verify_oauth2_token(auth_token,
            requests.Request(),
            settings.GOOGLE_API_TOKEN)

        (user, created)  = User.objects.get_or_create(
                email=idinfo['email'],
                defaults={
                    'first_name':idinfo['given_name'],
                    'last_name':idinfo['family_name'],
                    'google_acc':idinfo['sub'],
                }
            )
        #user.save()
        (token, created) = Token.objects.get_or_create(user=user)
        user_data = {
            "email":user.email,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "google_acc":user.google_acc,
            "auth_token":token.key
        }
        return Response(user_data)
    except ValueError:
        return Response({
                'message': 'Invalid token'
            },
            status=status.HTTP_400_BAD_REQUEST)
    
class user_register_view(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerialiser

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            token, created = Token.objects.get_or_create(user=serializer.instance)
            return Response({'auth_token': token.key}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT) # change it to 
        
#fake endpoint
@api_view(['POST'])
def report_post_view(request):
    return Response({
                'message': 'Post reported'
            },
            status=status.HTTP_200_OK)
        