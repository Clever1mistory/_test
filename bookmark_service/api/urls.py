from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CollectionViewSet, BookmarkViewSet, AuthViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = router.urls
