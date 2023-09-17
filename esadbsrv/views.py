from django.shortcuts import render

projectsectionmenu = {
    'ОРГАНИЗАЦИИ':'formmethod=get formaction=/organization/',
    'ОБЪЕКТЫ':'formmethod=get formaction=/einst/', 
    'ГТП':'',
    }

schemesectionmenu = {
    'ЦЕНТРЫ ПИТАНИЯ':'formmethod=get formaction=/rmnode/',
    'ПРИСОЕДИНЕНИЯ':'', 
    'ГТП':'',
    }

equipmentsectionmenu = {
    'СЧЕТЧИКИ':'formmethod=get formaction=/meter/',
    'СПРАВОЧНИК СЧЕТЧИКОВ':'formmethod=get formaction=/atcmeterdir/',
    'ИЗМЕРИТЕЛЬНЫЕ ТТ ТН': 'formmethod=get formaction=/ttnexample/', 
    'СПРАВОЧНИК ТТ ТН':'formmethod=get formaction=/atcttndirectory/', 
    'УСТРОЙСТВА СВЯЗИ':'formmethod=get formaction=/commdevice/',
    'СПРАВОЧНИК УСТРОЙСТВ СВЯЗИ':'formmethod=get formaction=/cddirectory/', 
    'КАНАЛЫ СВЯЗИ':'formmethod=get formaction=/channel/', 
    }

staffsectionmenu = {
    'ОРГАНИЗАЦИИ':'formmethod=get formaction=/organization/',
#    'ПРОЕКТЫ':'formmethod=get formaction=/project/', 
    'КОНТАКТЫ':'formmethod=get formaction=/contact/', 
    'АЛЬБОМЫ':'formmethod=get formaction=/albumstore/',
#    'GDisk':'formmethod=get formaction=/gdiskstorage/',
#    'NextCloud':'formmethod=get formaction=/nxcstorage/',
    'ДОКУМЕНТЫ':'formmethod=get formaction=/docstore/',
    'ИИК':'formmethod=get formaction=/mic/',
    'ОБОРУДОВАНИЕ':'formmethod=get formaction=/equipment/',
    'ИМПОРТ СПР-КА ТТ ТН':'formmethod=get formaction=/atcttndirectoryimport/',
    'ИМПОРТ СПР-КА СЧЕТЧИКОВ':'formmethod=get formaction=/atcmeterdirimport/',
    'ИМПОРТ УСТРОЙСТВ СВЯЗИ':'formmethod=get formaction=/commdeviceimport/',
    }

def index(request):
    return render(request, 'index.html', 
        context = {'subtitle': 'Проект', 
            'data_from_view': 'Контекст Проекта',
            'contextmenu': projectsectionmenu}
        )

def equipment(request):
    return render(request, 'index.html', 
        context = {'subtitle': 'Оборудование', 
            'data_from_view': 'Сведения об оборудовании вне зависисмоcти от контекста Проекта', 
            'contextmenu': equipmentsectionmenu}
        )

def media(request):
    return render(request, 'index.html', 
        context = {'subtitle': 'Медиа', 
            'data_from_view': 'Медиа', 
            'contextmenu': mediasectionmenu}
        )

def staff(request):
    return render(request, 'index.html', 
        context = {'subtitle': 'Сервис', 
            'data_from_view': 'Только для технического персонала', 
            'contextmenu': staffsectionmenu}
        )

def about(request):
    return render(request, 'index.html', 
        context = {'subtitle': 'О сайте', 
            'data_from_view': 'Сайт информационой системы ESADB. Информационная поддержка проектов АИИС КУЭ', 
            'contextmenu': {}}
        )
