from django.db import models

class Category(models.Model):
   name = models.CharField(max_length=200)
   def __str__(self):
     return self.name

class Book(models.Model):
   name = models.CharField(max_length=200)
   price = models.IntegerField(default=0)
   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   author_name = models.CharField(max_length=200)
   def __str__(self):
     return self.name