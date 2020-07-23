# django_lr_loader/management/commands/match_images_to_file_system
import sys
from pathlib import Path
from collections import Counter
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError, OperationalError, IntegrityError
from django_lr_loader.models import LightroomCatalog, LightroomImageFileInfo, ImageToFileInfo
from django_fs_searcher.models import FileInfo

class Command(BaseCommand):
    help = """Matches images found by 'get_lightroom_catalog' to images (if possible) in the file lists collected by get_file_system in django-filesystem-searcher, another Django application.  Potential and positive image matches between Lightroom catalogs and file system data are stored in the database for later analysis."""
    lr_hostname = None
    fs_hostname = None
    fs_volume = None
    lrcat_hostname = None
    lrcat_volume = None
    verbose = False


    def add_arguments(self, parser):
        parser.add_argument("--lr_hostname", help="Limit matches to Lightroom hostname.", default=None)
        parser.add_argument("--fs_hostname", help="Limit matches to file system hostname.", default=None)
        parser.add_argument("--fs_volume", help="Limit matches to file system volume.", default=None)
        parser.add_argument("--lrcat_hostname", help="Hostname where working Lightroom catalog is located.")
        parser.add_argument("--lrcat_volume", help="Volume where working Lightroom catalog is located.")

    def certainty(self, hashes=[], matches=[]):
        distinct_hash_counts = Counter(hashes)

        if self.verbose:
            print("\tMatches", len(matches), "Hashes", len(hashes), "Distinct Hashes", len(distinct_hash_counts.keys()))

        for match in matches:
            match.certainty = int(100.0 * distinct_hash_counts[match.file_info.dropbox_hash] / len(hashes))
            match.save()

            if (
                match.certainty > 50 and 'Pictures' in match.file_info.full_path and
                match.lightroom_image_file_info.status != LightroomImageFileInfo.Status.FILE_EXISTS_IN_PICTURES
            ):
                if (
                    self.lrcat_hostname and self.lrcat_hostname == match.file_info.hostname and
                    self.lrcat_volume   and self.lrcat_volume   == match.file_info.volume
                ):
                    match.lightroom_image_file_info.status = LightroomImageFileInfo.Status.FILE_EXISTS_IN_PICTURES
                    match.lightroom_image_file_info.save()
                elif match.lightroom_image_file_info.status == LightroomImageFileInfo.Status.UNKNOWN:
                    match.lightroom_image_file_info.status = LightroomImageFileInfo.Status.FILE_EXISTS_ON_BACKUP
                    match.lightroom_image_file_info.save()

            if self.verbose:
                print(f"\tMatch id {match.lightroom_image_file_info.id}::{match.file_info.id}", file=sys.stderr)
                print(f"\tfile_name {match.lightroom_image_file_info.print_path}::{match.file_info.full_path}", file=sys.stderr)
                print(f"\tCertainty {match.certainty}", f"Status {match.lightroom_image_file_info.status}", sys.stderr)

    def handle(self, *args, **options):
        self.lr_hostname = options['lr_hostname']
        self.fs_hostname = options['fs_hostname']
        self.fs_volume = options['fs_volume']
        self.lrcat_hostname = options['lrcat_hostname']
        self.lrcat_volume = options['lrcat_volume']
        self.verbose = True if options['verbosity'] else False

        if self.verbose:
            print('lr_hostname', self.lr_hostname, file=sys.stderr)
            print('fs_hostname', self.fs_hostname, file=sys.stderr)
            print('fs_volume', self.fs_volume, file=sys.stderr)
            print('lrcat_hostname', self.lrcat_hostname, file=sys.stderr)
            print('lrcat_volume', self.lrcat_volume, file=sys.stderr)

        if self.lr_hostname:
            lr_queryset = LightroomImageFileInfo.objects.filter(hostname=self.lr_hostname)
        else:
            lr_queryset = LightroomImageFileInfo.objects.all()

        fs_queryset = FileInfo.objects
        if not self.fs_hostname and not self.fs_volume:
            fs_queryset = fs_queryset.all()
        if self.fs_hostname:
            fs_queryset = fs_queryset.filter(hostname=self.fs_hostname)
        if self.fs_volume:
            fs_queryset = fs_queryset.filter(volume=self.fs_volume)

        for lightroom_image_file_info in lr_queryset:
            path = lightroom_image_file_info.print_path
            if path[1] == ':':
                # Remove assumed Windows Drive Letter
                path = path[2:]
            if path[0] == '/':
                path = path[1:]
            if path.startswith('Pictures/'):
                path = path[9:]
            if self.verbose:
                print(path, sys.stderr)

            hashes = []
            matches = []

            for file_info in fs_queryset.filter(file_name=lightroom_image_file_info.file_original_name):
                if file_info.full_path.endswith(path):
                    hashes.append(file_info.dropbox_hash)
                    matches.append(
                        ImageToFileInfo(
                           lightroom_catalog=lightroom_image_file_info.lightroom_catalog,
                           lightroom_image_file_info=lightroom_image_file_info,
                           file_info=file_info,
                           certainty=0
                        )
                    )

            self.certainty(hashes=hashes, matches=matches)


