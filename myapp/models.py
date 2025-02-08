from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    description=models.CharField(max_length=250)
    body=models.TextField()
    published_on=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)


