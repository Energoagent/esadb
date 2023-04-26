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
        
    def fldlist():
        dict1 = ['ИИК', 'МОДЕЛЬ', 'БП', 'СЕР_НОМЕР', 'СПРАВОЧНИК', 'ДАТА_ВЫП', 'ДАТА_ПОВ', 'КЛ_Т', 'КАНАЛЫ', 'ИНФОРМАЦИЯ', 'ПРИМЕЧАНИЕ', 'ДОКУМЕНТЫ']
        return dict1

    def valuelist(self):
        if self.mtrdir == None: str2 = '-'
        else: str2 = self.mtrdir.regnumber
        if self.classae == None: str1 = '-'
        else: str1 = self.classae
        if self.classre == None: str1 = str1 + '/-'
        else: str1 = str1 + '/' + self.classae
        if self.channelae == None: str3 = '-'
        else: str3 = self.channelae
        if self.channelre == None: str3 = str3 + '/-'
        else: str3 = str3 + '/' + self.channelre
        lst1 = [self.id, self.mtrmodel, self.bl, self.sn, str2, self.fbdate, self.cldate, str1, str3, self.info, self.note]
        doclist = []
        for doc in self.docs.all():
            doclist.append(doc.__str__() + '; \n')
        lst1.append(str(doclist))
        return lst1
