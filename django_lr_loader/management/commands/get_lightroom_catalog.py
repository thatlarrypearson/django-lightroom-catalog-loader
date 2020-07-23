# django-lightroom/src/management/commands/get_lightroom_catalog.py
import sys
import socket
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError, OperationalError, IntegrityError
from lr_reader import LightroomFileFinder
from django_lr_loader.models import LightroomCatalog, LightroomImageFileInfo

class Command(BaseCommand):
    help = 'Searches a file system and loads file information into the database'

    def add_arguments(self, parser):
        parser.add_argument(
                "base_paths",
                nargs='+',
                metavar="base_path",
                help="Relative or absolute file path to Adobe Lightroom SQLite Database, example: Pictures/Lightroom/Lightroom Catalog.lrcat"
            )
        parser.add_argument(
                "--is_archive",
                help="Adobe Lightroom SQLite Databases are backups.",
                default=False,
                action='store_true'
            )
 
    def handle(self, *args, **options):
        hostname = socket.gethostname()
        current_working_directory = Path.cwd()
        is_backup = options['is_backup']
        verbose = True if options['verbosity'] else False

        for base_path in options['base_paths']:
            path = Path(base_path)
            if path.is_absolute():
                absolute_path = path
            else:
                absolute_path = current_working_directory.drive / current_working_directory / base_path

            if not absolute_path.is_file():
                raise FileNotFoundError(f"Not a File: {absolute_path}")

            lightroom_catalog = LightroomCatalog(
                hostname=hostname,
                database_file_name=absolute_path.name,
                full_database_file_path=str(absolute_path),
                is_backup=is_backup
            )
            lightroom_catalog.save()

            if verbose:
                print("base_path:", base_path, file=sys.stderr)
                print("absolute_path:", absolute_path, file=sys.stderr)
                print("verbosity:", options['verbosity'], "\n", file=sys.stderr)

            records = LightroomFileFinder(base_path, verbose=verbose)

            for record in records:
                if not record['folder_path_from_root']:
                    record['folder_path_from_root'] = ''
                if not record['root_rel_path_from_catalog']:
                    record['root_rel_path_from_catalog'] = ''
                record['file_extension'] = (record['file_extension']).lower()

                record['print_path'] = f"{record['root_name']}/{record['folder_path_from_root']}{record['file_original_name']}"
                record['lightroom_catalog'] = lightroom_catalog
                if verbose:
                    print(record['print_path'], file=sys.stderr)
                lightroom_image_file_info = LightroomImageFileInfo(**record)
                try:
                    lightroom_image_file_info.save()
                except (DataError, OperationalError, IntegrityError) as e:
                    print("EXCEPTION", e, file=sys.stderr)

