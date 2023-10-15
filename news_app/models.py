# librarys
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.urls import reverse

# model Manager
class Publish(models.Manager):
  def get_queryset(self):
    return super().get_queryset().filter(status=News.Status.Publish)



# Category Model
class Category(models.Model):
  name = models.CharField(max_length=150)

  def __str__(self):
    return self.name
  


# News Model

class News(models.Model):

  class Status(models.TextChoices):
    Draft = 'DF',"Draft"
    Publish = "PB","Publish"


  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250)
  image = models.ImageField(upload_to='news/images')
  category = models.ForeignKey(Category,on_delete=models.CASCADE)
  body = models.TextField()
  published_time = models.DateTimeField(default=timezone.now)
  created_time = models.DateTimeField(auto_now_add=True)
  updated_time = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=2,choices=Status.choices,default=Status.Draft)

  object = models.Manager()
  publish = Publish()
  def __str__(self):
    return self.title
  class Meta:
    ordering = ["-published_time"]
  def get_absolute_url(self):
    return reverse('news_detail',args=[self.slug])


class Contact(models.Model):
  name = models.CharField(max_length=150)
  email = models.EmailField(max_length=150)
  message = models.TextField()

  def __str__(self):
    return self.email
  
class Photography(models.Model):
  image = models.ImageField(upload_to='photo/image')


class Comments(models.Model):
  news = models.ForeignKey(News,on_delete=models.CASCADE,related_name='comments')
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
  body = models.TextField()
  active = models.BooleanField(default=True)
  created_time = models.DateTimeField(auto_now_add=True)


  class Meta:
    ordering = ['-created_time']
  def __str__(self):
    return f"Comments - {self.news} "