from imdb_app.models import MovieList, OttPlatform, Review, UserProfile
from rest_framework import serializers

    
class OttPlatformSerializer(serializers.ModelSerializer):
    movielist = serializers.StringRelatedField(many=True, read_only = True)
    class Meta:
        model = OttPlatform
        fields = '__all__'
        

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('review_movie_name',)
        
        
class MovieListSerializer(serializers.ModelSerializer):
    ott_platfor_name = serializers.CharField(source='ott_platfor_name.ott_name')
    category = serializers.MultipleChoiceField(choices=MovieList.CATEGOTY_CHOICES,  allow_blank=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = MovieList
        fields = ('id', 'movie_name', 'category', 'cast', 'date_of_movie_release', 'ott_platfor_name', 'avg_rating', 'number_of_ratings', 'reviews')

    def create(self, validated_data):
        ott_name = validated_data.pop('ott_platfor_name')['ott_name']
        category = validated_data.pop('category', [])
        ott_platform = OttPlatform.objects.get(ott_name=ott_name)
        movie = MovieList.objects.create(ott_platfor_name=ott_platform, **validated_data)
        # if category:
        movie.category = category
        movie.save()
        return movie

    def validate_ott_platfor_name(self, value):
        allowed_ott_names = [ott.ott_name for ott in OttPlatform.objects.all()]
        if value not in allowed_ott_names:
            raise serializers.ValidationError(f"Invalid ott platform name. Allowed names: {', '.join(allowed_ott_names)}.")
        return value
    
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_name.username')
    category = serializers.MultipleChoiceField(choices=MovieList.CATEGOTY_CHOICES)
    class Meta:
        model = UserProfile
        fields = ('id', 'user_name','email', 'date_of_birth', 'category')
        
    def create(self, validated_data):
        username = validated_data.pop('user_name')['username']
        user = User.objects.get(username=username)
        profile = UserProfile.objects.create(user_name=user, **validated_data)
        return profile
        
    # def create(self, validated_data):
    #     category_data = validated_data.pop('category')
    #     userprofile = UserProfile.objects.create(**validated_data)

    #     # Retrieve the Category instances based on the category names
    #     categories = []
    #     for category in category_data:
    #         category_name = category['category_name']
    #         category_instance = Category.objects.get_or_create(category_name=category_name)[0]
    #         categories.append(category_instance)

    #     # Assign the categories to the userprofile
    #     userprofile.category.set(categories)

    #     return userprofile
