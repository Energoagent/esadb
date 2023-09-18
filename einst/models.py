from django.db import models

from albumstore.models import AlbumStore
from docstore.models import DocStore
from channel.models import Channel
from commdevice.models import CommDevice
from org.models import Organization
from project.models import Project
from contact.models import Contact

class EInst(models.Model):
    class Meta:
        verbose_name = 'Объект, электроустановка, сооружение, подстанция'
    name = models.CharField(max_length = 200, help_text = '', verbose_name = 'Наименование')
    adress = models.CharField(max_length = 200, help_text = '', verbose_name = 'Адрес', blank = True, null = True)
    owner = models.ForeignKey(Organization, on_delete = models.SET_NULL, null = True)
    project = models.ForeignKey(Project, on_delete = models.SET_NULL, null = True)
    contacts = models.ManyToManyField(Contact)
    contactinfo = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Контакты', blank = True, null = True)
    info = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Общая информация', blank = True, null = True)
    note = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
    albums = models.ManyToManyField(AlbumStore)
    commdevices = models.ManyToManyField(CommDevice)
    channels = models.ManyToManyField(Channel)
    
    def __str__(self):
        if self.name == None:
            s1 = '-'
        else: s1 = self.name
        return s1
        
    def get_absolute_url(self):
        u1 = f'/einst/{self.pk}/'
        return u1

