# django_file_system_searcher/urls.py
from django.urls import path
from django.views.generic import TemplateView
from .views import LightroomImageFileInfoViewSet, LightroomCatalogViewSet, ImageToFileInfoViewSet

urlpatterns = [
    path('', TemplateView.as_view(template_name="LightroomCatalogFileInfo-index.html"), name='index'),

    path('lightroom_catalog_file_info/', LightroomImageFileInfoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('lightroom_catalog_file_info/<int:pk>/', LightroomImageFileInfoViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('lightroom_catalog/', LightroomCatalogViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('lightroom_catalog/<int:pk>/', LightroomCatalogViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
    path('image_to_file_info/', ImageToFileInfoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('image_to_file_info/<int:pk>/', ImageToFileInfoViewSet.as_view({
                                                'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy',
                                            })
    ),
]
