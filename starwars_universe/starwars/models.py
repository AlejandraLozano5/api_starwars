from django.db import models

# Create your models here.
class Planet(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['name']
        #db_table    =   'planets'
        #managed     =   True

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=200)
    opening_text = models.CharField(max_length=1000)
    planets = models.ManyToManyField(Planet)
    director = models.CharField(max_length=200)
    producer = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Personage(models.Model):
    name = models.CharField(max_length=200)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name