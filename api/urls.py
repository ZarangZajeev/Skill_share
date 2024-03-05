from django.urls import path

from api import views

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()
router.register("userprofile",views.UserProfileURView,basename="userprofiles")
router.register("product",views.ProdcutCreateReadUpdateDeleteView,basename="products")
router.register("cart/item",views.CartItemView,basename="cartitems")
router.register("cart",views.CartView,basename="cart")
router.register('comment/(?P<product_id>\d+)',views.CommentView, basename='comment')
router.register('product/bids/(?P<product_id>\d+)',views.BidAddView,basename="bidadd")
router.register('bids',views.BidView,basename="bids")


from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns=[
   path('register/',views.SignUpView.as_view()),
   path('token/',ObtainAuthToken.as_view()),
   path('swagger/',schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]+router.urls