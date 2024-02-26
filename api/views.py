from django.shortcuts import render

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework.parsers import MultiPartParser, FormParser


from api.models import UserProfile,Product

from api.serializers import UserProfileSerializer,ProductSerializer


from api.serializers import UserSerializer

# url: http://127.0.0.1:8000/api/register/
class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
# url: http://127.0.0.1:8000/api/userprofile/
    
class UserProfileURView(viewsets.ModelViewSet):
    serializer_class=UserProfileSerializer
    queryset=UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission denied")
    
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission denied")
    
# url: http://127.0.0.1:8000/api/product/
class ProdcutCreateReadUpdateDeleteView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=ProductSerializer
    queryset=Product.objects.all()

    def perform_create(self, serializer):
        # Associate the user making the request with the product
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        # Get the product instance
        instance = self.get_object()

        # Check if the user making the request is the same user who added the product
        if request.user == instance.user:
            # Proceed with the update
            return super().update(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)