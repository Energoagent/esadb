import os
from pathlib import Path

import openpyxl

from channel.models import Channel

def channel_import():

    ''' импорт каналов связи из нормализованного файла Excel
    в каталоге import
    дублирование устройств связи не коннтролируется - сделать позже'''
    
    try:
        basedir = Path(__file__).resolve().parent.parent
        imppath = os.path.join(basedir, 'import\КАНАЛЫ_СВЯЗИ.xlsx')
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
            newch = Channel(
                name = '',
                bl = '',
                chtype = row[4].value,
                ccid = row[0].value,
                number = row[1].value,
                ip = row[2].value,
                operator = row[5].value,
                config = row[10].value,
                info = '',
#                note = row[13].value,
                )
            newch.save()
        return True