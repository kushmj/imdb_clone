from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from imdb_app.api.views import MovieListViewSet, OttListViewSet, ReviewList,ReviewRetriveUpdateDestroyView, ReviewCreate, UserProfileViewset

router = DefaultRouter()
router.register('lists', MovieListViewSet, basename='lists')
router.register('ottplatforms', OttListViewSet, basename='ott')
# router.register('category', CategoryViewset, basename = 'category')
router.register('userprofile', UserProfileViewset, basename= 'userprofile')



urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name = 'review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name= 'review-list'),
    path('reviews/<int:pk>/', ReviewRetriveUpdateDestroyView.as_view(), name = 'review-retrive-update-delete'),
    
]
