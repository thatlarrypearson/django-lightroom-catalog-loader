# django-lightroom/src/models.py
from django.db import models
from django_fs_searcher.models import FileInfo


class LightroomCatalog(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    hostname = models.CharField(blank=True, verbose_name='hostnames', max_length=128)
    database_file_name = models.CharField(verbose_name='database_file_name', max_length=4096, db_index=True)
    full_database_file_path = models.CharField(verbose_name='full_database_file_paths', max_length=4096)
    is_backup = models.BooleanField(default=False, verbose_name='is_backup')
    created = models.DateTimeField(auto_now_add=True)


class LightroomImageFileInfo(models.Model):
    class Status(models.IntegerChoices):
        FILE_EXISTS_IN_PICTURES = 1
        FILE_EXISTS_ON_BACKUP = 2
        UNKNOWN = 3

    id = models.BigAutoField(primary_key=True, db_index=True)
    lightroom_catalog = models.ForeignKey(LightroomCatalog, on_delete=models.PROTECT, verbose_name='lightroom_catalog')
    status = models.IntegerField(choices=Status.choices, default=Status.UNKNOWN)
    root_id = models.BigIntegerField(verbose_name='root_id')
    folder_id = models.BigIntegerField(verbose_name='folder_id')
    file_id = models.BigIntegerField(verbose_name='file_id')
    root_name   = models.CharField(verbose_name='root_name', max_length=4096)
    folder_path_from_root = models.CharField(blank=True, verbose_name='folder_path_from_root', max_length=4096)
    root_absolute_path = models.CharField(verbose_name='root_absolute_path', max_length=4096)
    file_original_name = models.CharField(verbose_name='file_original_name', max_length=4096, db_index=True)
    root_rel_path_from_catalog = models.CharField(verbose_name='root_rel_path_from_catalog', max_length=4096)
    file_base_name = models.CharField(verbose_name='file_base_name', max_length=4096)
    file_extension = models.CharField(verbose_name='file_extension', max_length=4096)
    print_path = models.CharField(verbose_name='print_path', max_length=4096)


class ImageToFileInfo(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    lightroom_catalog = models.ForeignKey(
        LightroomCatalog, on_delete=models.PROTECT, verbose_name='lightroom_catalog'
    )
    lightroom_image_file_info = models.ForeignKey(
        LightroomImageFileInfo, on_delete=models.PROTECT, verbose_name='lightroom_image_file_info',
        db_index=True
    )
    file_info = models.ForeignKey(
        FileInfo, on_delete=models.PROTECT, verbose_name='file_info',
        db_index=True
    )
    certainty = models.IntegerField(verbose_name="certainty", default=0)
    created = models.DateTimeField(auto_now_add=True)
