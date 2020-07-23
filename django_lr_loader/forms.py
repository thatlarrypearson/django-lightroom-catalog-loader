from django.forms import ModelForm
from .models import LightroomImageFileInfo, LightroomCatalog, ImageToFileInfo
 
class LightroomImageFileInfoForm(ModelForm):
    class Meta:
        model = LightroomImageFileInfo
        fields = [
            "lightroom_catalog", "status", 
            "root_id",  "folder_id", "file_id",
            "root_name", "root_rel_path_from_catalog",
            "folder_path_from_root", "relative_path", "root_absolute_path",
            "file_original_name", "file_base_name", "file_extension",
            "print_path",
        ]

class LightroomCatalogForm(ModelForm):
    class Meta:
        model = LightroomCatalog
        fields = [
            'parent', 'hostname', 'database_file_name', 'full_database_file_path',
            'is_backup',
        ]

class ImageToFileInfoForm(ModelForm):
    class Meta:
        model = ImageToFileInfo
        fields = [
            "lightroom_catalog", "lightroom_image_file_info", "file_info", "certainty",
        ]