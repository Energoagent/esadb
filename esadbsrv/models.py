import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from pathlib import Path

balance = [
    ('', ''),
    ('абонент', 'абонент'),
    ('сети', 'сети'),
    ('сбыт', 'сбыт'),
    ]
    
def balancetodict(balance):
    dict1 = {}
    for it1 in balance:
        dict1[it1[0]] = it1[1]
    return dict1

balancedict = balancetodict(balance)
        
class CDDirectory(models.Model):
    class Meta:
        verbose_name = 'Справочник: устройства связи, УСПД, контроллеры'
    cdtype = models.CharField(max_length = 256, help_text = '', verbose_name = 'Тип устройства', blank = False, default = '')
    model = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модель устройства', blank = True, null = True)
    fabric = models.CharField(max_length = 256, help_text = '', verbose_name = 'Завод-изготовитель', blank = True, null = True)
    info = models.CharField(max_length = 256, help_text = '', verbose_name = 'Информация', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)

    def __str__(self):
        if self.cdtype == None: s1 = ''
        else: s1 = self.cdtype
        if self.model == None: s1 = s1 + ''
        else: s1 = s1 + ' ' + self.model
        return s1
        
    def get_absolute_url(self):
        u1 = f'/cddirectory/{self.id}/'
        return u1

class ATCTTNDirectory(models.Model):
    class Meta:
        verbose_name = 'Справочник АТС измерительных трансформаторов'
    code = models.CharField(max_length = 256, help_text = '', verbose_name = 'Синтетический код справочника АТС',  unique = True)
    ttntype = models.CharField(max_length = 256, help_text = '', verbose_name = 'Тип устройства')
    model = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модель трансформатора')
    regnumber = models.CharField(max_length = 256, help_text = '', verbose_name = 'Номер в Госреестре СИ')
    modification = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модификация трансформатора', blank = True, null = True)
    pclass = models.CharField(max_length = 256, help_text = '', verbose_name = 'Класс точности трансформатора', blank = True, null = True)
    primarycoil = models.CharField(max_length = 256, help_text = '', verbose_name = 'Первичная обмотка', blank = True, null = True)
    secondarycoil = models.CharField(max_length = 256, help_text = '', verbose_name = 'Вторичная обмотка', blank = True, null = True)
    colibrationint = models.CharField(max_length = 256, help_text = '', verbose_name = 'Межповерочный интервал', blank = True, null = True)
    fabric = models.CharField(max_length = 256, help_text = '', verbose_name = 'Завод-изготовитель', blank = True, null = True)
    sn = models.CharField(max_length = 256, help_text = '', verbose_name = 'Серийный номер', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    
    def __str__(self):
        return self.model + ' ' + self.regnumber
        
    def get_absolute_url(self):
        u1 = f'/atcttndirectory/{self.pk}/'
        return u1

class ATCMeterDir(models.Model):
    class Meta:
        verbose_name = 'Справочник измерительных приборов АТС'
    model = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модель ИП')
    code = models.CharField(max_length = 256, help_text = '', verbose_name = 'Код АТС', unique = True)
    regnumber = models.CharField(max_length = 256, help_text = '', verbose_name = 'Номер в Госреестре СИ')
    calibrationint = models.CharField(max_length = 256, help_text = '', verbose_name = 'Межповерочный интервал', blank = True, null = True)
    modification = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модификация ИП', blank = True, null = True)
    classae = models.CharField(max_length = 8, help_text = '', verbose_name = 'Класс точности активной энергии', blank = True, null = True)
    classre = models.CharField(max_length = 8, help_text = '', verbose_name = 'Класс точности реактивной энергии', blank = True, null = True)
    channelae = models.CharField(max_length = 8, help_text = '', verbose_name = 'Измерительные каналы активной энергии', blank = True, null = True)
    channelre = models.CharField(max_length = 8, help_text = '', verbose_name = 'Измерительные каналы реактивной энергии', blank = True, null = True)
    fabricator = models.CharField(max_length = 256, help_text = '', verbose_name = 'Завод-изготовитель', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)

    def __str__(self):
        return self.model + ': ' +self.regnumber
        
    def get_absolute_url(self):
        return f'/atcipdirectory/{self.pk}/'

       

