from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from pathlib import Path
import xlrd
import os
from django.contrib.auth.decorators import login_required

from esadbsrv.models import ATCMeterDir
from esadbsrv.viewmods.viewcommon import CompleteListView

# справочник счетчиков АО АТС

@login_required
def atsmeterdirimport(request):
    '''
    импорт справочника сетчиков АТС

    импорт из нормализованной таблицы Excel плученой с сайта АТС
    режим исполнения - синхронный
    '''
    basedir = Path(__file__).resolve().parent.parent.parent
    impdir = os.path.join(basedir, 'import')
    os.chdir(impdir)
    rb = xlrd.open_workbook('АТС_СПРАВОЧНИК_ИП.xls', formatting_info=True)
    sheet = rb.sheet_by_index(0)
    print(sheet)
    for  i in range(sheet.nrows):
        if i == 0:
            shtitle = sheet.row_values(i)
        else:
            try:
                rv = sheet.row_values(i)
                md = ATCMeterDir( 
                    model = rv[3],
                    code = rv[4],
                    regnumber = rv[1], 
                    calibrationint = rv[0],
                    modification = rv[9], 
                    classae = rv[12], 
                    classre = rv[13],
                    channelae = rv[8],
                    channelre = rv[10],
                    fabricator = rv[7], 
                    note = rv[5])
                md.save()
            except Exception as e:
                pass
    return HttpResponseRedirect(reverse_lazy('atcmeterdir'))
    
class ATCMeterDirListView(CompleteListView):
    model = ATCMeterDir
    template_name = 'atcmeterdir/atcmeterdir_list.html'
    paginate_by = 10
    ordering = 'model'
    subtitle = 'Оборудование: справочник счетчиков АТС'
    contextmenu = {'Просмотреть': 'formmethod=GET formaction=detail/'}
    filterkeylist = {'Модель':'model', 'Изготовитель':'fabricator','номер в ГРСИ':'regnumber'}
  
def atcmeterdirdetailview(request):
    if request.method == 'GET':
        mdid = request.GET.get('mdid')
        if mdid != None:
            meterdir = ATCMeterDir.objects.get(id = mdid)
            context = {'status':'', 'meterdir':meterdir,
                'contextmenu':{'Вернуться':'formmethod=GET formaction=../'}, 
                'subtitle':'Оборудование: Справочник счетчиков АТС'}
            return render(request, 'atcmeterdir/atcmeterdir_detail.html', context = context)
    return redirect('../')



