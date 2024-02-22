from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to="profile_pics",null=True)
    bio=models.CharField(max_length=200)
    options=(
        ("drawing","drawing"),
        ("communication","communication"),
        ("crafting","crafting"),
        ("coding","coding"),
    )
    skills=models.CharField(max_length=200,choices=options)

    def __str__(self):
        return self.name
    
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    media=models.FileField(upload_to="product_media")
    description=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart")
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def cart_items(self):
        qs=self.cartitem.all()
        return qs
    
    @property
    def cart_total(self):
        cart_items=self.cart_items
        if cart_items:
            total=sum([item.total for item in cart_items])
            return total
        else:
            return 0
def create_cart(sender,insatnce,created,**kwargs):
    if created:
        Cart.objects.create(user=insatnce)

class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cartitem")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

post_save.connect(create_profile,sender=User)
post_save.connect(create_cart,sender=User)