from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status

from rest_framework.decorators import action
from rest_framework.response import Response

from .utils import get_and_authenticate_user, create_user_account
from .logic import get_open_graph_data
from .models import Collection, Bookmark
from .serializers import CollectionSerializer, BookmarkSerializer, \
                        UserLoginSerializer, AuthUserSerializer, UserRegisterSerializer

from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated, AllowAny


@swagger_auto_schema()
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@swagger_auto_schema()
class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def create_bookmark(self, request, pk=None):
        link = request.data.get('link')  # Получаем ссылку на статью из POST запроса

        if link:
            try:
                og_data = get_open_graph_data(link)  # Получаем данные с помощью функции get_open_graph_data

                # Создаем новую закладку с полученными данными
                bookmark = Bookmark.objects.create(
                    title=og_data['title'],
                    description=og_data['description'],
                    url=link,
                    link_type='website',
                    preview_image=og_data['image'],
                    user=request.user,  # Предполагается, что пользователь авторизован
                    collection=None
                    # Если нужно добавить закладку в коллекцию, указать соответствующий объект Collection
                )

                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'No link provided'})

    @action(detail=True, methods=['post'])
    def remove_from_collection(self, request, pk=None):
        bookmark = self.get_object()
        bookmark.collection = None
        bookmark.save()
        serializer = self.get_serializer(bookmark)
        return Response(serializer.data)


@swagger_auto_schema()
class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


@swagger_auto_schema()
class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = UserRegisterSerializer(request.user)
        return Response(serializer.data)
