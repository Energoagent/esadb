import os
from django.conf import settings
from django.db import models

ALBUM_DIR = 'albumstore'



def albumpath():
    ap = os.path.join(settings.MEDIA_ROOT, ALBUM_DIR)
    return ap

class AlbumStore(models.Model):
    class Meta:
        verbose_name = 'Альбом изображений'
    local = models.BooleanField(default = True)
    name = models.CharField(max_length = 256, help_text = '', verbose_name = 'Наименование', blank = True, null = True)
    folder = models.FilePathField(path = albumpath, verbose_name = 'Папка', recursive=True, allow_files=False, allow_folders=True, max_length=100)
    info = models.CharField(max_length = 256, help_text = '', verbose_name = 'Информация', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)

    def __str__(self):
        return self.name + ':' + str(self.id)
      
    def get_absolute_url(self):
        u1 = f'albumstore/{self.pk}'
        return u1

    def delete(self):
        super().delete()

    def get_url(self):
        if local:
            return settings.MEDIA_URL +'/' + ALBUM_DIR + '/' + self.folder
        else:
            return ASCLOUD_URL +'/' + ALBUM_DIR + '/' + self.folder

    def get_path(self):
        return os.path.join(settings.MEDIA_ROOT, ALBUM_DIR, self.folder)

