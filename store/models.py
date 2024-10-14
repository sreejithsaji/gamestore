from django.db import models

from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField

from django.db.models.signals import post_save  

from django.db.models import Sum



class UserProfile(models.Model):

    bio=models.CharField(max_length=260,null=True)

    profile_pic=models.ImageField(upload_to="profile_pictures",default="/profile_pictures/default.png")

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:

        return self.user_object.username
    

class Tag(models.Model):

    title=models.CharField(max_length=200,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:

        return self.title


class Project(models.Model):

    title=models.CharField(max_length=200)

    description=models.TextField()

    developer=models.CharField(max_length=200)

    publisher=models.CharField(max_length=200)

    release_year=models.CharField(max_length=200)

    tag_objects=models.ManyToManyField(Tag)

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="projects")

    thumbnail=EmbedVideoField()

    game_pic=models.ImageField(upload_to="game_pictures",default="game_pictures/default.png")

    price=models.PositiveIntegerField()

    files=models.FileField(upload_to="projects",null=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def downloads(self):

        return OrderSummary.objects.filter(is_paid=True,project_object=self).count()

    def __str__(self) -> str:

        return self.title



class Cart(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def cart_total(self):

        return self.basket_items.filter(is_order_placed=False).values("project_object__price").aggregate(total=Sum("project_object__price")).get("total")


class CartItems(models.Model):

    cart_object=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="basket_items")

    project_object=models.ForeignKey(Project,on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)



class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    project_object=models.ManyToManyField(Project)

    order_id=models.CharField(max_length=200,null=True)

    is_paid=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    total=models.FloatField(null=True)





def create_profile(sender,instance,created,*args,**kwargs):

    if created:

        UserProfile.objects.create(user_object=instance)


post_save.connect(sender=User,receiver=create_profile)


def create_basket(sender,instance,created,*args,**kwargs):
    if created:
        Cart.objects.create(owner=instance)
post_save.connect(sender=User,receiver=create_basket)

