from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
# Create your models here.

class OttPlatform(models.Model):
    ott_name = models.CharField(max_length=100)
    about = models.CharField(max_length=1000)
    website_url = models.URLField(max_length=500)
    
    def __str__(self):
        return self.ott_name
    
class MovieList(models.Model):
    CATEGOTY_CHOICES = (
    ("Action", "Action"),
    ('Adventure','Adventure'),
    ('Drama','Drama'),
    ('Comedy', "Comedy"),
    ("RPG", "RPG"),
    ("Horror", "Horror"),
    ('Romance','Romance'),
    ('Fantasy','Fantasy'),
)
    movie_name = models.CharField(max_length=200)
    category = MultiSelectField(max_length=100, choices=CATEGOTY_CHOICES)
    ott_platfor_name = models.ForeignKey(OttPlatform, on_delete=models.CASCADE, related_name='movielist')
    cast = models.CharField(max_length=100)
    date_of_movie_release = models.DateField()
    avg_rating = models.FloatField(default=0)
    number_of_ratings = models.IntegerField(default=0)
    
    def __str__(self):
        return self.movie_name
    
    
class UserProfile(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    date_of_birth = models.DateField()
    category = MultiSelectField(max_length=100, choices=MovieList.CATEGOTY_CHOICES)
    
    def __str__ (self):
        return str(self.user_name) 
        
    
class Review(models.Model):
    review_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review_movie_name =models.ForeignKey(MovieList, on_delete=models.CASCADE, related_name = 'reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " | " + self.review_movie_name.movie_name

