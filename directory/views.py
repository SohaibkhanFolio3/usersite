from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from directory import serializers
from directory import models
from rest_framework import filters
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from rest_framework.authentication import TokenAuthentication
from directory import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        an_apiview = {"one": []}
        return Response({"msg": "Hello", "an_apiview": an_apiview})

    def post(self, request, format=None):
        """Create a hello msg with name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer._validated_data.get("name")
            email = serializer._validated_data.get("email")
            message = f"Hello {name} \n Email {email}"
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({"method": "PUT"})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({"method": "PATCH"})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({"method": "DELETE"})


class HelloViewSet(viewsets.ViewSet):
    """Creating viewsets for the test api"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            "uses Actions (list, create , update,partial_update)",
            "Autmatically maps to url using routers ",
            "provides more functionality with less code",
        ]
        return Response({"message": "Hello!", "a_viewset": a_viewset})

    def create(self, request):
        """Create anew hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            email = serializer.validated_data.get("email")
            message = f"Name is {name} , Email is {email}"
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({"http_method": "GET"})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({"http_method": "PUT"})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({"http_method": "PATCH"})

    def delete(self, request, pk=None):
        user = get_object_or_404(models.UserProfile, id=pk)
        
        # Check if the user has permission to delete the profile
        self.check_object_permissions(request, user)
        
        user.delete()

        return Response({"message": "User deleted successfully"})


class UserprofileViewSet(viewsets.ViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    
    def list(self, request):
        users = self.queryset
        user_list = [
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
            }
            for user in users
        ]
        return Response({ "users": user_list})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            s_name = serializer.validated_data.get("name")
            s_email = serializer.validated_data.get("email")
            s_password = serializer.validated_data.get('password')
            user = serializer.create(validated_data=dict(name=s_name, password=s_password , email= s_email))
            
            # Serialize the user object as a list and then serialize to JSON
            serialized_user = serialize('json', [user])
            userdata =             {
                "id": user.id,
                "email": user.email,
                "name": user.name,  
            }

            return Response({"message": 'Profile Created', 'user': userdata})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = get_object_or_404(models.UserProfile, id=pk)
        user.delete()

        return Response({"message": "User deleted successfully"})
        
    def retrieve(self, request, pk=None):
        user = get_object_or_404(models.UserProfile, id=pk)
        serializer = self.serializer_class(user)

        return Response(serializer.data)  
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})
          



class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    '''Handle Creating User authentication token'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


