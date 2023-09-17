from django.db import models

from docstore.models import DocStore

class Channel(models.Model):
    class Meta:
        verbose_name = 'Канал связи'
    name = models.CharField(max_length = 256, help_text = '', verbose_name = 'Наименование', blank = True, null = True)
    bl = models.CharField(max_length = 256, help_text = '', verbose_name = 'Принадлежность', blank = True, null = True)
    chtype = models.CharField(max_length = 256, help_text = '', verbose_name = 'Тип', blank = True, null = True)
    ccid = models.CharField(max_length = 64, help_text = '', verbose_name = 'Идентификатор', blank = True, null = True)
    number = models.CharField(max_length = 64, help_text = '', verbose_name = 'Номер', blank = True, null = True)
    ip = models.CharField(max_length = 64, help_text = '', verbose_name = 'IP адрес: порт', blank = True, null = True)
    operator = models.CharField(max_length = 256, help_text = '', verbose_name = 'Оператор', blank = True, null = True)
    config = models.CharField(max_length = 256, help_text = '', verbose_name = 'Конфигурация', blank = True, null = True)
    info = models.CharField(max_length = 1024, help_text = '', verbose_name = 'Информация', blank = True, null = True)
    note = models.CharField(max_length = 1024, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
    
    def __str__(self):
        if self.name == None:
            s1 = '-'
        else: s1 = self.name
        return s1
        
    def get_absolute_url(self):
        u1 = f'/channel/{self.pk}/'
        return u1

