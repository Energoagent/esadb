from django.db import models

from albumstore.models import AlbumStore
from docstore.models import DocStore

class Contact(models.Model):
    class Meta:
        verbose_name = 'Контакт'
    name = models.CharField(max_length = 200, help_text = '', verbose_name = 'ФИО')
    contactinfo = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Контактная информация: телефон e-mail и тд', blank = True, null = True)
    info = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Общая информация', blank = True, null = True)
    note = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
    
    def __str__(self):
        if self.name == None:
            s1 = '-'
        else: s1 = self.name
        return s1
        
    def get_absolute_url(self):
        u1 = f'/contact/{self.pk}/'
        return u1

