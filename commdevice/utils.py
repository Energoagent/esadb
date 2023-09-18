import os
from pathlib import Path

import openpyxl

from commdevice.models import CommDevice

def commdevice_import():

    ''' импорт устройств связи из нормализованного файла Excel
    в каталоге import
    дублирование устройств связи не коннтролируется - сделать позже'''
    
    try:
        basedir = Path(__file__).resolve().parent.parent
        imppath = os.path.join(basedir, 'import\УСТРОЙСТВА_СВЯЗИ.xlsx')
        wb = openpyxl.load_workbook(imppath)
        sheet = wb.get_sheet_by_name('_')
    except Exception as e:
        print('ESADB:Exception:', e)
        return False
    else:
        if sheet == None: 
            print('ESADB:Exception:import source not opend')
            return False
        for row in sheet["A2:L%d" % sheet.max_row]:
            newdevice = CommDevice(
                bl = '',
                sn = row[0].value,
                cdmodel = row[4].value,
#                fbdate = row[1], подобрать формат даты в исходной Ecel таблице
                addrtype = 'm2m port',
                addr = row[7].value,
                config = row[9].value,
                info = row[10].value,
                note = row[11].value,
                )
            newdevice.save()
        return True