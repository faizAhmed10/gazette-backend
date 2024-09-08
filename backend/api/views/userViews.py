from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from api.serializers.userSerializer import *
from django.contrib.auth.models import User 
from api.models import *
from api.views.articleViews import check_author
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    try:
        data = request.data
        username = data['username']
        if User.objects.filter(username = username).exists():
            raise Exception("Username already exists, try a different username")
        
        if User.objects.filter(email = data[email]).exists():
            raise Exception("Cannot create multiple accounts of the same Email")
        
        serializer = UserRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'details':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = {'details': str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def create_author(request):
    try:
        data = request.data
        name = data['name']
        
        
        if not AllowAuthor.objects.filter(name=name).exists():
            raise Exception("This author is not allowed.")

        if Authors.objects.filter(name=name).exists():
            raise Exception("Author with this name already exists.")
        
        serializer = AuthorRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = {'details': str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_my_profile(request):
    author = request.user
    try:
        
        if check_author(author):
            author_instance = Authors.objects.get(user=author)
            serializer = AuthorSerializer(author_instance, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You are not a registered author"}, status=status.HTTP_401_UNAUTHORIZED)
    
    except Authors.DoesNotExist:
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])   
def is_author(request):
    user = request.user
    try:
        if Authors.objects.filter(user=user).exists():
            return Response("Author Verified",status=status.HTTP_200_OK)
        else:
            return Response("You are not a Registered Author", status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        message = {'details': str(e)}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  