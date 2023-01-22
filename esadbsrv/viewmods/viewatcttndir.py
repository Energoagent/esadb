from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from pathlib import Path
from django.views import generic
import xlrd
import os
from django.db import connection
from django.contrib.auth.decorators import login_required

from esadbsrv.models import ATCTTNDirectory
from esadbsrv.viewmods.viewcommon import CompleteListView

@login_required
def atcttndirectoryimport(request):
    basedir = Path(__file__).resolve().parent.parent.parent
    impdir = os.path.join(basedir, 'import')
    os.chdir(impdir)
    rb = xlrd.open_workbook('АТС_СПРАВОЧНИК_ТТН.xls', formatting_info=True)
    sheet = rb.sheet_by_index(0)
    for  i in range(sheet.nrows):
        if i == 0:
            shtitle = sheet.row_values(i)
        else:
            rv = sheet.row_values(i)
            try:
                ttn1 = ATCTTNDirectory(
                    code = rv[0], 
                    ttntype = rv[1], 
                    model = rv[2],
                    regnumber = rv[3], 
                    modification = rv[4], 
                    pclass = rv[5],
                    primarycoil = rv[6], 
                    secondarycoil = rv[7],
                    colibrationint = rv[8], 
                    fabric = rv[9], 
                    sn = rv[10], 
                    note = rv[11])
                ttn1.save()
            except:
                pass
    return HttpResponseRedirect(reverse_lazy('atcttndir'))

class ATCTTNDirectoryListView(CompleteListView):
    model = ATCTTNDirectory
    template_name = 'atcttndir/atcttndirectory_list.html'
    paginate_by = 10
    ordering = 'model'
    subtitle = 'Оборудование: справочник измерительных трансформаторов АТС'
    contextmenu = {'Просмотреть': 'formmethod=GET formaction=detail/',
        'Вернуться':'formmethod=GET formaction=../'}
    filterkeylist = {'Сброс':'', 'Модель':'model', 'Изготовитель':'fabric', 'номер в ГРСИ':'regnumber'}
    is_filtered = True

def atcttndirectorydetailview(request):
    if request.method == 'GET':
        ttndirid = request.GET.get('ttndirid')
        if ttndirid != None:
            ttndir = ATCTTNDirectory.objects.get(id = ttndirid)
            context = {'status':'', 'ttndir':ttndir,
                'contextmenu':{'Вернуться':'formmethod=GET formaction=../'}, 
                'subtitle':'Оборудование: справочник измерительных трансформаторов АТС'}
            return render(request, 'atcttndir/atcttndirectory_detail.html', context = context)
    return redirect('../')

