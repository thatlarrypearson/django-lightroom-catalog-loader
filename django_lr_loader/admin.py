from django.contrib import admin
from .models import LightroomCatalog, LightroomImageFileInfo, ImageToFileInfo

admin.site.site_header = "Lightroom Catalog Image File Finder"

@admin.register(LightroomCatalog)
class LightroomCatalogAdmin(admin.ModelAdmin):
    fields = [
        'parent', 'hostname', 'database_file_name', 'full_database_file_path',
        'is_backup',
    ]
    readonly_fields = ['id', 'created', ]
    search_fields = ['database_file_name', ]

@admin.register(LightroomImageFileInfo)
class LightroomImageFileInfoAdmin(admin.ModelAdmin):
    fields = [
        "lightroom_catalog", "status",
        "root_id",  "folder_id", "file_id",
        "root_name", "root_rel_path_from_catalog",
        "folder_path_from_root", "root_absolute_path",
        "file_original_name", "file_base_name", "file_extension",
        "print_path",
    ]
    readonly_fields = ['id', ]
    search_fields = ['file_original_name', ]


@admin.register(ImageToFileInfo)
class ImageToFileInfoAdmin(admin.ModelAdmin):
    fields = [
        "lightroom_catalog", "lightroom_image_file_info", "file_info", "certainty",
    ]
    readonly_fields = ["id", "created", ]
    search_fields = [
        'lightroom_image_file_info__file_original_name',
        'file_info__file_name',
        'lightroom_catalog__database_file_name',
    ]


