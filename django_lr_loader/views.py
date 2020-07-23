# django_file_system_searcher/view.py
from rest_framework import viewsets
import django_filters.rest_framework
from rest_framework.permissions import IsAuthenticated
from .models import LightroomImageFileInfo, LightroomCatalog, ImageToFileInfo
from .serializers import LightroomImageFileInfoSerializer, LightroomCatalogSerializer, ImageToFileInfoSerializer


class LightroomImageFileInfoViewSet(viewsets.ModelViewSet):
    serializer_class = LightroomImageFileInfoSerializer
    model = LightroomImageFileInfo
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['file_original_name', ]
    queryset = LightroomImageFileInfo.objects.all()


class LightroomCatalogViewSet(viewsets.ModelViewSet):
    serializer_class = LightroomCatalogSerializer
    model = LightroomCatalog
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['database_file_name', ]
    queryset = LightroomCatalog.objects.all()


class ImageToFileInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ImageToFileInfoSerializer
    model = ImageToFileInfo
    permission_classes = [IsAuthenticated, ]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_fields = ['lightroom_image_file_info', 'file_info', ]
    queryset = ImageToFileInfo.objects.all()
