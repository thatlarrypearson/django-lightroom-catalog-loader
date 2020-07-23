# django_file_system_searcher/serializers.py
from rest_framework import serializers
from .models import LightroomImageFileInfo, LightroomCatalog, ImageToFileInfo


class LightroomImageFileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightroomImageFileInfo
        fields = [
            "lightroom_catalog",
            "id", "status",
            "root_id",  "folder_id", "file_id",
            "root_name", "root_rel_path_from_catalog",
            "folder_path_from_root", "root_absolute_path",
            "file_original_name", "file_base_name", "file_extension",
            "print_path",
        ]


class LightroomCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightroomCatalog
        fields = [
            "id", "parent",
            "hostname", "database_file_name", "full_database_file_path", "is_backup",
            "created",
        ]


class ImageToFileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageToFileInfo
        fields = [
            "id", "lightroom_catalog", "lightroom_image_file_info", "file_info",
            "certainty", "created", 
        ]