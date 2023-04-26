import os
from django.db import models
from docstore.models import DocStore
from einst.models import EInst
from channel.models import Channel



class MIC(models.Model):
    class Meta:
        verbose_name = 'ИИК'
    name = models.CharField(max_length = 256, help_text = '', verbose_name = 'Наименование', blank = True, null = True)
    code = models.CharField(max_length = 256, help_text = '', verbose_name = 'Код АТС', blank = True, null = True)
    einst = models.ForeignKey(EInst, on_delete = models.SET_NULL, null = True)
    schnum = models.CharField(max_length = 256, help_text = '', verbose_name = 'Номер на схеме', blank = True, null = True)
    info = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Общая информация', blank = True, null = True)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
    channels = models.ManyToManyField(Channel)
     
    def __str__(self):
        if self.name != None:
            return self.name
        else:
            return '-'
        
    def get_absolute_url(self):
        return f'/ttnexample/{self.pk}/'
        
    def fldlist():
        lst1 = ['НАИМЕНОВАНИЕ', 'КОД АТС', 'НОМЕР НА СХЕМЕ', 'ИНФОРМАЦИЯ', 'ПРИМЕЧАНИЕ', 'ДОКУМЕНТЫ']
        return lst1

    def valuelist(self):
        lst1 = [self.name, self.code, self.schnum, self.info, self.note]
        doclist = []
        for doc in self.docs.all():
            doclist.append(doc.__str__())
        lst1.append('; \n'.join(doclist))
        return lst1

