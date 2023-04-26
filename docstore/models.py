import os
from django.db import models
from django.conf import settings

documenttype = [
    ('', ''),
    ('договор', 'договор'),
    ('АРБП', 'АРБП'),
    ('АТП', 'АТП'),
    ('однолинейная схема', 'однолинейная схема'),
    ('акт приемки узлов учета', 'акт приемки узлов учета'),
    ('паспорт', 'паспорт'),
    ('св-во о поверке', 'св-во о поверке'),
    ('фото без крышки', 'фото без крышки'),
    ('отчет', 'отчет'),
    ('прочие', 'прочие'),
    ]
    
def doctypetodict(documenttype):
    dict1 = {}
    for it1 in documenttype:
        dict1[it1[0]] = it1[1]
    return dict1

dtdict = doctypetodict(documenttype)

class DocStore(models.Model):
    class Meta:
        verbose_name = 'Документ'
    doctype = models.CharField(max_length = 64, help_text = '', verbose_name = 'Тип документа', choices = documenttype)
    name = models.CharField(max_length = 256, help_text = '', verbose_name = 'Наименование', validators='', blank = True, null = True)
    number = models.CharField(max_length = 64, help_text = '', verbose_name = 'Номер', validators='', blank = True, null = True)
    date = models.DateField(help_text = '', verbose_name = 'Дата', blank = True, null = True)
    docfile = models.FileField(upload_to='docstore', verbose_name = 'Файл', max_length = 256)
    note = models.CharField(max_length = 256, help_text = '', verbose_name = 'Примечание', validators='', blank = True, null = True)

    def __str__(self):
        return str(self.doctype) + ':' + str(self.name) + ':' + str(self.number)
        
    def as_string(self):
       return str(self.doctype) + ':' + str(self.name) + ':' + str(self.number)
  
    def get_absolute_url(self):
        return f'docstore/{self.pk}'
        
    def delete(self):
        self.docfile.delete(save = False)
        super().delete()

    def get_url(self):
        u1 = settings.MEDIA_URL + self.get_absolute_url()
        return u1

    def get_path(self):
        u1 = os.path.join(settings.MEDIA_ROOT, 'docstore/', self.docfile)
        return u1
