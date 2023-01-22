from django.db import models
from django.contrib.auth.models import User

from docstore.models import DocStore
from contact.models import Contact

class Project(models.Model):
    class Meta:
        verbose_name = 'Проект'
    name = models.CharField(max_length = 200, help_text = '', verbose_name = 'Наименование')
    info = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Общая информация', blank = True, null = True)
    note = models.CharField(max_length = 1000, help_text = '', verbose_name = 'Примечание', blank = True, null = True)
    docs = models.ManyToManyField(DocStore)
    contacts = models.ManyToManyField(Contact)
    users = models.ManyToManyField(User)
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        u1 = f'/project/{self.pk}/'
        return u1

