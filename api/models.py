from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to="profile_pics",default='default.png',null=True)
    bio=models.CharField(max_length=200)
    options=(
        ("drawing","drawing"),
        ("communication","communication"),
        ("crafting","crafting"),
        ("coding","coding"),
    )
    skills=models.CharField(max_length=200,choices=options)
    user_skill=models.CharField(max_length=200,null=True)

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
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def cart_items(self):
        qs = self.cart_items.all()
        return qs
    
    @property
    def cart_total(self):
        cart_items = self.cart_items.all()
        if cart_items:
            total = sum([item.total for item in cart_items])
            return total
        else:
            return 0
def create_cart(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(user=instance)

class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.qty*self.product.price
    
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment")
    text=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    product=models.ForeignKey(Product,related_name="post_comments",on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bids")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    amount=models.PositiveIntegerField()
    bids_options=(
        ("Pending","pending"),
        ("Accept","accept"),
        ("Reject","reject"),
    )
    status=models.CharField(max_length=200,choices=bids_options,default="Pending")

    def __str__(self):
        return self.amount


class Chat(models.Model):
    send_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="send_user")
    receiver_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver_user")
    message=models.CharField(max_length=500)
    image=models.ImageField(upload_to="chat_image",null=True)
    created_date=created_date=models.DateTimeField(auto_now_add=True)


    def _str_(self):
        return self.message
    
post_save.connect(create_profile,sender=User)
post_save.connect(create_cart,sender=User)
