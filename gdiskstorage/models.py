import os
from datetime import date
from django.conf import settings
from django.db import models
from django.utils import timezone

GDISK_PATH = 'gdiskstorage'

class GDiskFolder(models.Model):
    class Meta:
        verbose_name = 'Папка на Google disk'
    name = models.CharField(max_length = 256, verbose_name = 'Наименование', blank = True, null = True)
    date = models.DateField(help_text = '', verbose_name = 'Дата', default = timezone.now, blank = True, null = True)
    folder = models.FilePathField(path = '', verbose_name = 'Папка', recursive = True, allow_files = False, allow_folders = True, max_length = 100)
    info = models.CharField(max_length = 256, verbose_name = 'Информация', blank = True, null = True)
    note = models.CharField(max_length = 256, verbose_name = 'Примечание', blank = True, null = True)

    def __str__(self):
        return self.name + ':' + str(self.id)
      
    def get_absolute_url(self):
        u1 = f'gdiskfolder/{self.pk}'
        return u1

    def delete(self):
# add code for delete folder on google drive
        super().delete()


