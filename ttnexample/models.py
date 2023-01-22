from django.db import models

from mic.models import MIC
from esadbsrv.models import ATCTTNDirectory, balance
from docstore.models import DocStore

ttntypelist = [
    ('Трансформатор тока', 'Трансформатор тока'),
    ('Трансформатор напряжения', 'Трансформатор напряжения'),
    ('Трансформатор комбинированный', 'Трансформатор комбинированный'),
    ('ИП прочие', 'ИП прочие'),
    ]

phase = [
    ('', ''),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('A-B', 'A-B'),
    ('B-C', 'B-C'),
    ('A-C', 'A-C'),
    ('A-B-C', 'A-B-C'),
    ]
    
def phasetodict(phase):
    dict1 = {}
    for it1 in phase:
        dict1[it1[0]] = it1[1]
    return dict1

phasedict = phasetodict(phase)


class TTNExample(models.Model):
    class Meta:
        verbose_name = 'Измерительный трансформатор'
    mic = models.ForeignKey(MIC, on_delete = models.SET_NULL, null = True)
    ttntype = models.CharField(max_length = 64, help_text = '', verbose_name = 'Тип устроства', choices = ttntypelist, blank = True, null = True)
    ph = models.CharField(max_length = 64, help_text = '', verbose_name = 'Фаза', choices = phase, blank = True, null = True)
    bl = models.CharField(max_length = 64, help_text = '', verbose_name = 'Принадлежность', choices = balance, blank = True, null = True)
    sn = models.CharField(max_length = 64, help_text = '', verbose_name = 'Заводской номер', blank = True, null = True)
    ttnmodel = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модель', blank = True, null = True)
    ttndir = models.ForeignKey(ATCTTNDirectory, on_delete = models.SET_NULL, null = True)
    fbdate = models.DateField(help_text = '', verbose_name = 'Дата выпуска', blank = True, null = True)
    cldate = models.DateField(help_text = '', verbose_name = 'Дата поверки', blank = True, null = True)
    primarycoil = models.CharField(max_length = 256, help_text = '', verbose_name = 'Первичная обмотка', blank = True, null = True)
    secondarycoil = models.CharField(max_length = 256, help_text = '', verbose_name = 'Вторичная обмотка', blank = True, null = True)
    pclass = models.CharField(max_length = 256, help_text = '', verbose_name = 'Класс точности трансформатора', blank = True, null = True)
    info = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Общая информация', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
     
    def __str__(self):
        if self.ttnmodel == None: s1 = '-'
        else: s1 = self.ttnmodel
        if self.sn == None: s2 = '-'
        else: s2 = self.sn
        return s1 + ' SN:' + s2
        
    def get_absolute_url(self):
        return f'/ttnexample/{self.pk}/'

    def fldlist():
        lst1 = ['ИИК', 'УСТРОЙСТВО', 'ФАЗА', 'БП', 'СЕР НОМЕР', 'МОДЕЛЬ', 'СПРАВОЧНИК', 'ДАТА ВЫП', 'ДАТА ПОВ', 
            'КТ', 'КЛ Т', 'ИНФОРМАЦИЯ', 'ПРИМЕЧАНИЕ']
        return lst1

    def valuelist(self):
        if self.ttndir == None: rn = '-'
        else: rn = self.ttndir.regnumber
        if self.primarycoil == None: kt = '-'
        else: kt = self.primarycoil
        if self.secondarycoil == None: kt = kt + '/-'
        else: kt = kt + '/' + self.secondarycoil
        lst1 = [self.mic.name, self.ttntype, self.ph, self.bl, self.sn, self.ttnmodel, rn, 
            self.fbdate, self.cldate,kt, self.pclass, self.note ,self.info, self.note]
        return lst1

