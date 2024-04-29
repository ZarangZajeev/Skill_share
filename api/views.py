from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from exam.models import Answer

from api.models import UserProfile,Product,Cart,CartItems,Comment,Bids,Chat,User
from api.serializers import UserProfileSerializer,ProductSerializer,CartItemSerializer,CartSerializer
from api.serializers import UserSerializer,CommentSerializer,BidsSerializer,ChatSerializer

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class   ObtainTokenView(APIView):
    permission_classes = [AllowAny]  # Allow any user to obtain a token

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=400)

        # Perform authentication
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=400)

        # Create or retrieve token
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user_id': user.id})

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
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

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

    # def create(self, request, *args, **kwargs):
    #     # Get the user's Answer status
    #     answer_status = Answer.objects.filter(user=request.user).first()

    #     # Check if the user has passed the exam
    #     if answer_status and answer_status.status == "pass":
    #         return super().create(request, *args, **kwargs)
    #     else:
    #         return Response({"detail": "User hasn't passed the exam. Cannot create a product."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        # Get the product instance
        instance = self.get_object()
        # Check if the user making the request is the same user who added the product
        if request.user == instance.user:
            # Proceed with the update
            return super().update(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=403)
        
    # url: http://127.0.0.1:8000/api/product/{id}/add_to_cart/
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product_obj = Product.objects.get(id=product_id)
        # Get or create a cart for the user
        cart_obj, created = Cart.objects.get_or_create(user=request.user)
        # Create a mutable copy of request.data
        mutable_data = request.data.copy()
        # Set the cart field in the mutable copy
        mutable_data['cart'] = cart_obj.id
        serializer = CartItemSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save(product=product_obj)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

# url: localhost:8000/api/cart/
class CartView(viewsets.ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=request.user.cart
        serializer=CartSerializer(qs,many=False)
        return Response(data=serializer.data)
    
class CartItemView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=CartItemSerializer
    queryset=CartItems.objects.all()

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission Deneid")

class CommentView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=CommentSerializer
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Comment.objects.filter(product_id=product_id)


    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(user=self.request.user, product_id=product_id)

# Bid add view
class BidAddView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=BidsSerializer
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Comment.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(user=self.request.user, product_id=product_id)

# Bid view
class BidView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=BidsSerializer
    queryset=Bids.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Bids.objects.filter(user=user) | Bids.objects.filter(product__user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Chat
class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes =[authentication.TokenAuthentication]

    def perform_create(self, serializer):
        sender_user = self.request.user  # Extract sender user from the authentication token
        receiver_user_id = self.kwargs.get('receiver_id')
        receiver_user = get_object_or_404(User, id=receiver_user_id)

        serializer.save(send_user=sender_user, receiver_user=receiver_user)

    def get_queryset(self):
        sender_user = self.request.user  # Extract sender user from the authentication token
        receiver_user_id = self.kwargs.get('receiver_id')
        receiver_user = get_object_or_404(User, id=receiver_user_id)

        queryset = Chat.objects.filter(send_user=sender_user, receiver_user=receiver_user)
        return queryset
    
# Chat list view
class UserChatMessagesAPIView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user = self.request.user  # Get the authenticated user
        queryset = Chat.objects.filter(send_user=user) | Chat.objects.filter(receiver_user=user)
        return queryset
        

def get_products_by_category(request, category):
    if request.method == 'GET':
        # Query products based on the category
        products = Product.objects.filter(category=category)

        # Serialize products to JSON
        serialized_products = [{
            'user':product.user.id,
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'created_date': product.created_date,
            'link': product.link,
            # Add other fields if needed
        } for product in products]

        # Return the JSON response
        return JsonResponse({'products': serialized_products})
    else:
        # Return an error for unsupported HTTP methods
        return JsonResponse({'error': 'Only GET method is supported'}, status=405)