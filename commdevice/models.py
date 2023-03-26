from django.db import models

from esadbsrv.models import CDDirectory, balance
from einst.models import EInst
from docstore.models import DocStore

class CommDevice(models.Model):
    class Meta:
        verbose_name = 'Устройства связи, УСПД, контроллеры'
    einst = models.ForeignKey(EInst, on_delete = models.SET_NULL, null = True)
    bl = models.CharField(max_length = 64, help_text = '', verbose_name = 'Принадлежность', choices = balance)
    sn = models.CharField(max_length = 64, help_text = '', verbose_name = 'Заводской номер', blank = True, null = True)
    cdmodel = models.CharField(max_length = 256, help_text = '', verbose_name = 'Модель', blank = True, null = True)
    cddir = models.ForeignKey(CDDirectory, on_delete = models.SET_NULL, null = True)
    fbdate = models.DateField(help_text = '', verbose_name = 'Дата выпуска', blank = True, null = True)
    addr = models.CharField(max_length = 16, help_text = '', verbose_name = 'Сетевой адрес', blank = True, null = True)
    info = models.CharField(max_length = 256, help_text = '', verbose_name = 'Информация', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
     
    def __str__(self):
        if self.cddir.cdtype == None: s1 = ''
        else: s1 = self.cddir.cdtype
        if self.sn != None: s1 = s1 + ' SN' + self.sn 
        return s1
        
    def get_absolute_url(self):
        u1 = f'/commdevice/{self.pk}/'
        return u1

