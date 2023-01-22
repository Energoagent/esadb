from django.views import generic

def requestget(request, key):
    if request.method == 'POST': return request.POST.get(key)
    if request.method == 'GET': return request.GET.get(key)
    return None
        

class CompleteListView(generic.ListView):
    subtitle = ''
    contextmenu = {'Просмотреть': 'formmethod=GET formaction=detail/',
        'Добавить': 'formmethod=GET formaction=create/',
        'Изменить': 'formmethod=GET formaction=update/',
        'Удалить': 'formmethod=GET formaction=delete/',
        'Копировать': 'formmethod=GET formaction=copy/',
        'Вернуться': 'formmethod=GET formaction=../'}
    is_filtered = True
    filterkeylist = {'':'',}
    hiddeninput = ''
    def get_queryset(self):
        filterkey = self.request.GET.get('filterkey')
        filtervalue = self.request.GET.get('filtervalue')
        if filtervalue == None: filtervalue = ''
        if filterkey == None or filterkey == '':
            return super().get_queryset()
        else:
            filterkey = filterkey + '__icontains'
            dict1 = {filterkey: filtervalue}
            return super().get_queryset().filter(**dict1)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contextmenu'] = self.contextmenu
        context['filterkeylist'] = self.filterkeylist
        filterkey = self.request.GET.get('filterkey')
        if filterkey == None: filterkey = ''
        filtervalue = self.request.GET.get('filtervalue')
        if filtervalue == None: filtervalue = ''
        context['is_filtered'] = self.is_filtered
        context['filterkey'] = filterkey
        context['filtervalue'] = filtervalue
        context['subtitle'] = self.subtitle
        context['hiddeninput'] = self.hiddeninput
        return context
