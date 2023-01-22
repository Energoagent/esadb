from django.db import models

from docstore.models import DocStore
from contact.models import Contact

class Organization(models.Model):
    class Meta:
        verbose_name = 'Организация, юридическое лицо, ИП'
    name = models.CharField(max_length = 200, help_text = '', verbose_name = 'Наименование')
    inn = models.CharField(max_length = 10, serialize = False ,help_text = '', verbose_name = 'ИНН', blank = True, null = True)
    req = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Реквизиты', blank = True, null = True)
    addr = models.CharField(max_length = 256, help_text = '', verbose_name = 'Адрес', blank = True, null = True)
    contactinfo = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Контакты', blank = True, null = True)
    info = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Общая информация', blank = True, null = True)
    note = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
    contacts = models.ManyToManyField(Contact)
        
    def __str__(self):
        if self.name == None: s1 = '-'
        else: s1 = self.name
        if self.inn == None: s2 = '-'
        else: s2 = self.inn
        return s1 + ' ИНН:' + s2

    def get_absolute_url(self):
        u1 = f'/organization/{self.pk}/'
        return u1

