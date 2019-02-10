from django.db import models
import os
import random
from django.db.models.signals import pre_save,post_save
from ecomeerce.utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q
#functions for image filename and locations
def get_filename_ext(filepath):
    basename=os.path.basename(filepath)
    name,ext=os.path.splitext(basename)
    return name,ext

def upload_image_path(instance,filename):
    new_filename=random.randint(1,39000939)
    name,ext=get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "product/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
        )

#product model manager
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True)
    def search(self,query):
       lookups=Q(title__icontains=query)|Q(description__icontains=query)|Q(tag__title__icontains=query)
       return self.filter(lookups).distinct()
    
class ProductModelManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def all(self):
        return self.get_queryset().active()

    def  features(self):
        return self.get_queryset().featured()

    def get_by_id(self,id):
        qs=self.get_queryset().filter(id=id)
        if qs.count==1:
            return qs.first()
        return None 

    def search(self,query):
        lookups=Q(title__icontains=query)|Q(description__icontains=query)|Q(tag__title__icontains=query)
        return self.get_queryset().active().search(query)

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=120)
    description=models.TextField()
    slug=models.SlugField(unique=True,blank=True)
    price=models.DecimalField(decimal_places=2,max_digits=20,default=20.99)
    image=models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)


    objects=ProductModelManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse('products:detail',kwargs={"slug":self.slug})

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
# --------------------------------------------------------------------------------------------------------

class Comment(models.Model):
    post=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments',null=True,blank=True)
    author=models.CharField(max_length=20)
    text=models.TextField()
    created_date=models.DateTimeField()

    def __str__(self):
        return self.author
