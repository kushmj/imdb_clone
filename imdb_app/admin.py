from django.contrib import admin
from imdb_app.models import MovieList, OttPlatform, Review,UserProfile

# Register your models here.

admin.site.register(MovieList)
admin.site.register(OttPlatform)
admin.site.register(Review)
admin.site.register(UserProfile)
