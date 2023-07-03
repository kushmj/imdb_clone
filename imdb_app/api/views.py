from imdb_app.api.serializers import MovieListSerializer, OttPlatformSerializer, ReviewSerializer, UserProfileSerializer
from imdb_app.models import MovieList, OttPlatform, Review, UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import os
import logging
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from imdb_app.api.permissions import IsAdminOrReadonly, ReviewUserOrReadOnly
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from imdb_app.api.pagination import MovieListPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('imdb_app.api.views')

class MovieListViewSet(viewsets.ModelViewSet):
    queryset = MovieList.objects.all().order_by('id')
    serializer_class = MovieListSerializer
    permission_classes = [IsAdminOrReadonly]
    pagination_class = MovieListPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie_name']
    
    def list (self, request, *args, **kwrgs):
        try:
            movie = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(movie)
            if page is not None: 
                serializer = self.serializer_class(page, many=True)
                logger.info("Retrived movie details")
                return self.get_paginated_response (serializer.data)
        except Exception as e:
            logger.error(f'Error while fetching movie list : {str(e)}')
            return Response ({"Error":"Error occured while fetching movie list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            movie = MovieList.objects.get(pk=pk)
            serializer = self.serializer_class(movie)
            logger.info(f'Retrived movie detail of id {pk}')
            # print('details', movie.__dict__)
            return Response (serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error while fetching movie of id {pk} : {str(e)}')
            return Response ({"Error":"Error occured while fetching movie list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                movie = serializer.save()

                # Fetching the categories of the newly added movie
                movie_categories = set(movie.category)
                user_profiles = UserProfile.objects.all()
                # Fetching matching user profiles
                matching_users = [
                user_profile
                for user_profile in user_profiles
                    if set(user_profile.category).intersection(movie_categories)
                ]
                print('matchingusers',matching_users)
                print('moviecategory',movie_categories)
                # Loop through each user and send email notification
                for user in matching_users:
                    subject = "New Movie Release Notification"
                    message = f"A new movie of your favorite category has been released. Movie name: {movie.movie_name}. Please check it out."
                    from_email = settings.EMAIL_HOST_USER
                    send_mail(subject, message, from_email, [user.email])
                    logger.info(f"Mail sent successfully to email: {user.email}")

                logger.info("New movie detail created successfully")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Error occurred while creating a new movie: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Creation failed with exception: {str(e)}")
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
        
    def update(self, request, pk=None):
        try:
            movie = MovieList.objects.get(pk=pk)
            serializer = self.serializer_class(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.warning(f'Movie detail of id {pk} updated sucessfully')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f'Error occured while updating movie of id {pk}')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Updating of movie failed : {str(e)}')
            return Response ({"Error":"Error occured while updating movie list"}, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, pk=None):
        try:
            movie = MovieList.objects.get(pk=pk)
            serializer = self.serializer_class(movie, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger.warning(f'Movie detail of id {pk} partially updated ')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f'Error occured while partially updating movie of id {pk}')
                return Response(serializer.errors)
        except Exception as e:
            logger.error(f'Updating of movie failed : {str(e)}')
            return Response ({'Error': 'Error occured while partially updating movie'}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        try:
            movie = MovieList.objects.filter(pk=pk)
            movie.delete()
            logger.warning(f'Movie of id {pk} deleted sucessfully')
            return Response({f"Message": "Movie sucessfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'Error occred while deleting the movie {str(e)}')
            return Response ({"Error":"Error occured while deleting movie list"}, status=status.HTTP_400_BAD_REQUEST)

# views for ott plaform to oerform CRUD operations
class OttListViewSet(viewsets.ModelViewSet):
    queryset = OttPlatform.objects.all()
    serializer_class = OttPlatformSerializer
    
    def list(self, request):
        try:
            ott_platforms = OttPlatform.objects.all()
            serializer = self.serializer_class(ott_platforms, many = True)
            logger.info("Retrived OTT List sucessfully")
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occerd while fetching OTT list {str(e)}")
            return Response({"error" : "Error Occured while retriving all OTT list"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def retrieve(self, request, pk=None):
        try:
            ott_platforms = OttPlatform.objects.get(pk=pk)
            serializer = self.serializer_class(ott_platforms)
            logger.info(f"OTT of id {pk} retived sucessfully")
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occerd while retiving the OTT of ID {pk} : {str(e)}")
            return Response ({"error" : "Error occured while retriving OTT details"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self,request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info('New OTT detail is created')
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                logger.error(f"Error occerd while creating the OTT : {serializer.errors}")
                return Response({'Error':'Error while creating New OTT'}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error occerd while creating the OTT : {str(e)}")
            return Response({'Error' : 'Error while creating new OTT'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partial_update(self, request, pk=None):
        try: 
            ott_platforms = OttPlatform.objects.get(pk=pk)
            serializer = self.serializer_class(ott_platforms, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger.warning(f"Partially updated the OTT details of id {pk}")
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                logger.error(f"Error while updatig OTT of id {pk} : {serializer.errors}")
                return Response({'Error' : 'Error while updating OTT  details'}, status = status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error occerd while updating the OTT of id {pk} : {str(e)}")
            return Response({'Error' : 'Error while updating OTT details'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        try:
            ott_paltforms = OttPlatform.objects.filter(pk=pk)
            ott_paltforms.delete()
            logger.warning(f"OTT details of id {pk} is sucefully deleted")
            return Response({'Message' : 'OTT details sucessfully deleted'})
        except Exception as e:
            logger.error(f'Error while deleting the data {str(e)}')
            return Response({'Error' : 'Error while deleting the OTT detaisl'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    # To filter based on username 
    # filterset_fields = ['review_user__user_name__username']
    # to filter based in user id (PK)
    filterset_fields = ['review_user']
    
    def get_queryset(self):
        try:
            pk = self.kwargs['pk']
            movie = MovieList.objects.filter(pk=pk).first()
            if not movie:
                logger.error(f'Failed to retrive reviews for move id {pk} ')
                raise ValidationError({'error' : f'Movie does not exists for id {pk}'})
            logger.info(f'Retrived reviews for movie id {pk} ')
            return Review.objects.filter(review_movie_name = pk)
        except MovieList.DoesNotExist:
            logger.error(f'Failed to retrieve reviews for movie {pk} movie does not exist for that id')
            raise ValidationError({'error' : f'Movie does not exists for id {pk}'})
        # except Exception as e:
        #     logger.error(f'Error while fetching the data {str(e)}')
        #     return Response({'Error': 'Exception occured while fetching the data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        try:
            pk = self.kwargs.get('pk')
            movie = MovieList.objects.get(pk = pk)
            
            review_user = self.request.user.userprofile
            review_queryset = Review.objects.filter(review_movie_name = movie, review_user = review_user)
            
            # if user already given the review it will raise validation error
            if review_queryset.exists():
                logger.warning(f'User has already given the review for movie id {pk}')
                raise ValidationError({'error' : f'You have alredy given the review for movie id {pk}'})
            
            # adding avg_rating and number_of_ratings when users gives the review
            if movie.number_of_ratings == 0:
                movie.avg_rating = serializer.validated_data['rating']
            else:
                movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
                
            movie.number_of_ratings = movie.number_of_ratings + 1
            movie.save()
            
            serializer.save(review_movie_name = movie, review_user = review_user)
            
        except MovieList.DoesNotExist:
            logger.error(f"Failed to create a review for movie ID {pk}. Movie with ID {pk} does not exist.")
            raise NotFound(detail=f"Movie with ID {pk} does not exist.")
        
        # except Exception as e:
        #     logger.error(f"Failed to create review for movie {pk} : {str(e)}")
        #     return Response({"error": "Error occured while creating review"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
class ReviewRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [ReviewUserOrReadOnly]
    
    def retrieve(self, request, pk=None):
        try:
            review_list = Review.objects.get(pk=pk)
            serializer = self.serializer_class(review_list)
            logger.info(f'Retrived the review id {pk}')
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Review.DoesNotExist:
            logger.error(f'review of id does not exist{pk}')
            raise ValidationError({'erre':f"review of id {pk} does not exist"})
        
        except Exception as e:
            logger.error(f'Error while retriving the review of id {pk} : {str(e)}')
            return Response({'error' : 'Error while retriving the review '}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partial_update(self, request, pk=None):
        try:
            review_list = Review.objects.get(pk=pk)
            self.check_object_permissions(request, review_list)
            serializer = self.serializer_class(review_list, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.warning(f"Review details of id {pk} updated successfully")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Error while updating review of id {pk}")
                return Response({'Error': 'Error while updating the review'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error while updating the review of id {pk}: {str(e)}")
            return Response({'Error': 'Error while updating the review'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    # def perform_destroy(self, instance):
    #     pk = instance.pk
    #     try:
    #         instance.delete()
    #         logger.warning(f"Review detail of id {pk} deleted successfully")
    #         return Response( 'Deleted successfully')
    #     except Exception as e:
    #         logger.error(f"Failed to delete review detail of id {pk}: {e}")
    #         return Response({'error': 'Failed to delete review detail'}, status=500)
        
    def destroy(self,request, *args, **kwargs):   
        try:
            instance = self.get_object()
            pk = instance.pk
            self.perform_destroy(instance)
            logger.warning(f"Review detail of id {pk}  deleted successfully")
            return Response({"message": f"Deleted successfully of id {pk}."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Failed to delete review detail of id : {e}")
            return Response({'error': 'Failed to delete review detail'}, status=500)
    
from imdb_app.api.permissions import UserprofileOwnerOrReadonly
class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserprofileOwnerOrReadonly,]
    
    def list(self,request):
        return Response('This operation is not allowed')
    
    def retrieve(self, request, pk=None):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer =  self.serializer_class(user_profile)
            logger.info(f'User details of id {pk} is retrived')
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            logger.info(f"Error occured while retrivng the user details of id {pk} : {str(e)}")
            return Response({'error':'Error occured while retriving the user details'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partila_update(self,request,pk=None):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer = self.serializer_class(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.warning(f'user profile of id {pk} has updated')
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(f'Error while updating user deatil of id {pk}')
                return Response({'error':'Error occured while updating userprofile'}, status= status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'Error while updating user deatil of id {pk}: {str(e)}')
            return Response({'error':'Error occured while updating userprofile'}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self,request, pk=None):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            self.check_object_permissions(request, user_profile)
            user_profile.delete()
            logger.warning(f'user details of id {pk} deleted sucessfully')
            return Response({'message':'Your profile has deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error while deleting the userprofile {str(e)}')
            return Response({'error': 'Error while deleting the user data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
