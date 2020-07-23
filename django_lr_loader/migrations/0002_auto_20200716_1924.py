# Generated by Django 3.0.1 on 2020-07-16 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_lr_loader', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lightroomimagefileinfo',
            name='relative_path',
        ),
        migrations.AddField(
            model_name='lightroomimagefileinfo',
            name='folder_path_from_root',
            field=models.CharField(blank=True, max_length=4096, verbose_name='folder_path_from_root'),
        ),
    ]
