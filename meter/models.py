from django.db import models

from mic.models import MIC
from esadbsrv.models import ATCMeterDir, balance
from docstore.models import DocStore

class Meter(models.Model):
    class Meta:
        verbose_name = 'Счетчик, измерительный прибор'
    mic = models.ForeignKey(MIC, on_delete = models.SET_NULL, null = True)
    bl = models.CharField(max_length = 64, help_text = '', verbose_name = 'Принадлежность', choices = balance)
    sn = models.CharField(max_length = 64, help_text = '', verbose_name = 'Заводской номер', blank = True, null = True)
    mtrmodel = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модель', blank = True, null = True)
    mtrdir = models.ForeignKey(ATCMeterDir, on_delete = models.SET_NULL, null = True)
    fbdate = models.DateField(help_text = '', verbose_name = 'Дата выпуска', blank = True, null = True)
    cldate = models.DateField(help_text = '', verbose_name = 'Дата поверки', blank = True, null = True)
    classae = models.CharField(max_length = 8, help_text = '', verbose_name = 'Класс точности активной энергии', blank = True, null = True)
    classre = models.CharField(max_length = 8, help_text = '', verbose_name = 'Класс точности реактивной энергии', blank = True, null = True)
    channelae = models.CharField(max_length = 8, help_text = '', verbose_name = 'Измерительные каналы активной энергии', blank = True, null = True)
    channelre = models.CharField(max_length = 8, help_text = '', verbose_name = 'Измерительные каналы реактивной энергии', blank = True, null = True)
    info = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Общая информация', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
     
    def __str__(self):
        if self.mtrmodel == None: s1 = '-'
        else: s1 = self.mtrmodel
        if self.sn == None: s2 = '-'
        else: s2 = self.sn
        return s1 + ' SN:' + s2
        
    def get_absolute_url(self):
        return f'/meter/{self.pk}/'
        

