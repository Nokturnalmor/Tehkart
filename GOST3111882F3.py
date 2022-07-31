import Cust_Functions as F
#import TehKart as TK
import os
from PyQt5 import QtWidgets, QtCore, QtGui

def showDialog(self, msg):
    msgBox = QtWidgets.QMessageBox()
    msgBox.setIcon(QtWidgets.QMessageBox.Information)
    msgBox.setText(msg)
    msgBox.setWindowTitle("Внимание!")
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)  # | QtWidgets.QMessageBox.Cancel)
    returnValue = msgBox.exec()

def vigruzit2(obj):
    n_dse = obj.ui.lineEdit_dse
    n_tk = obj.ui.lineEdit_nntk
    if n_tk.text() == '':
        return
    ima = n_tk.text() + '_' + n_dse.text() + ".txt"
    if F.nalich_file(F.scfg("add_docs")) == False:
        showDialog(obj, 'Не найден каталог с ТК')
        return
    spisok_tk = F.otkr_f(F.scfg("add_docs") + os.sep + ima, False, '|',pickl=True,propuski=True)
    if spisok_tk == ['']:
        showDialog(obj, 'Не найдена ТК')
        return

    sp = []
    sp.append(F.vpis("ГОСТ 3.1118-82  ФОРМА 3  САПР  ", 65, ' ', ' ', 2))
    sp.append(F.vpis("-" * 63, 65))
    sp.append(':          :                      :                 :     :     :')
    sp.append(F.vpis("-" * 63, 65))
    sp.append(F.vpis("", 5, prz=' ') + F.vpis(n_dse.text(), 24) + 13 * " " + F.vpis(n_tk.text(), 23))
    sp.append(F.vpis("", 5, prz=' ') + F.vpis("", 24) + 13 * " " + F.vpis("", 23))
    sp.append(F.vpis("-" * 63, 65))
    nnomer_dse, nazv_dse = [x for x in spisok_tk[0][0].split('$')]
    sp.append(
        ':    ' + F.vpis(nazv_dse, 48) + F.vpis(spisok_tk[2], 5, '',
                                                                                                ':') + '   :   :')
    sp.append(F.vpis("-" * 63, 65))
    sp_mat1 = spisok_tk[11][10].split('{')
    mat1 = sp_mat1[0].split('$')

    if mat1 == ['']:
        mat_shap = ''
        kod_m = ''
        n_r = ''
    else:
        mat_shap = mat1[1]
        kod_m = mat1[2]
        n_r = mat1[3]
    sp.append(":М 01" + F.vpis(mat_shap, 60))
    sp.append(":    " + F.vpis("", 60))
    sp.append(F.vpis("-" * 63, 65))
    sp.append(":    :_____КОД____:_ЕВ:__МД__:__ЕН_:_Н._РАСХ.:__КИМ_:_КОМ__:_ГС_:")




    sp.append(':М 02:' + F.vpis("", 23, " ", " ", 1) + F.vpis(kod_m, 7, " ", " ") + F.vpis(n_r, 10, " ", " ") +
              F.vpis("", 6, " ", " ", 1) + ':           :')
    sp.append(F.vpis("-" * 63, 65))
    sp.append(':    :_КОД ЗАГОТ._:__ПРОФИЛЬ_И_РАЗМЕРЫ_:__КД_:__М3__:           :')
    sp.append(':M 03:            :                                 :           :')
    sp.append(F.vpis("-" * 63, 65))
    sp.append(':__В_:ЦЕХ:__УЧ._:_РМ:ОПЕР:______КОД,_НАИМЕНОВАНИЕ_ОПЕРАЦИИ______:')
    sp.append(':__Г_:__________________ОБОЗНАЧЕНИЕ__ДОКУМЕНТА__________________:')
    sp.append(':__Д_:______________КОД,_НАИМЕНОВАНИЕ ОБОРУДОВАНИЯ______________:')
    sp.append(':__Е_:_СМ:_ПРОФ.:_Р_:_УТ_:_КР:КОИД:_ЕН_:_ОП_:КШТ.:_Т_ПЗ_:_Т_ШТ._:')

    tk, km, es = [x for x in spisok_tk[1][0].split('/')]

    flag = 0
    for i in range(10, len(spisok_tk)):
        if spisok_tk[i][20] == '0' and flag == 1:
            break
        if spisok_tk[i][20] == '0':
            flag = 1
            data_r = spisok_tk[i][5]
            razr = spisok_tk[i][6]
            sp_doc_tk = spisok_tk[i][13].split('$')
            sp_doc_tk.insert(0, km + " / " + es)
            sp = vivod_telo_1(sp, "Д", sp_doc_tk)
        if spisok_tk[i][20] == '1':
            rc = spisok_tk[i][4]
            nom_op = spisok_tk[i][2]
            nazv = spisok_tk[i][0]
            sp = vivod_telo_1(sp, "В", '', rc, nom_op, nazv, prop=3)

            sp_doc_op = spisok_tk[i][13].split('$')
            sp = vivod_telo_1(sp, "Д", sp_doc_op, prop=0)

            oborud = spisok_tk[i][5]
            sp = vivod_telo_1(sp, "Г", " ", p1=oborud, prop=0)

            prof = spisok_tk[i][8]
            k_r = spisok_tk[i][9]
            koid = spisok_tk[i][11]
            ed_n = '1'
            t_pz = spisok_tk[i][6]
            t_sh = spisok_tk[i][7]
            sp = vivod_telo_1(sp, "Е", " ", prof, k_r, koid, ed_n, t_pz, t_sh, prop=1)
        if spisok_tk[i][20] == '2':
            sod = spisok_tk[i][0]
            sp = vivod_telo_1(sp, "О", " ", sod, prop=1)
            instrum = spisok_tk[i][12].split('$')
            osnast = spisok_tk[i][11].split('$')
            sp = vivod_telo_1(sp, "Т", instrum, prop=0)
            sp = vivod_telo_1(sp, "Т", osnast, prop=0)
    sp = obrezat_stroki(sp, 65)
    razr = spisok_tk[3][0].upper()
    dat = spisok_tk[4][0]
    prov = spisok_tk[5][0]
    norm = spisok_tk[6][0]
    m_eksp = spisok_tk[7][0]
    norm_k = spisok_tk[8][0]
    sp = vstavit_osn_nadp_1(sp, razr, dat, prov, norm, m_eksp, norm_k)
    sp = vstavit_shapku(sp, n_dse.text(), n_tk.text())
    sp = vstavit_osn_nadp(sp)
    sp = prostavit_num_strok(sp,22,30,76,63)
    sp = prostavit_num_stranic(sp)
    nach_km = len(sp)+1
    sp = shapka1_km(sp,spisok_tk)
    flag = 0
    for i in range(10, len(spisok_tk)):
        if spisok_tk[i][20] == '0' and flag == 1:
            break
        if spisok_tk[i][20] == '0':
            flag = 1
        if spisok_tk[i][20] == '1':

            rc = spisok_tk[i][4]
            nom_op = spisok_tk[i][2]
            #nazv = spisok_tk[i][0]
            sp = vivod_telo_1(sp, "В", '', rc, nom_op, "", prop=3)
            sp_op_mat = spisok_tk[i][10].split('{')
            sp = vivod_telo_1(sp, "М", sp_op_mat, prop=0)
    #for i in sp:
    #    print(i)
    sp = vstavit_osn_nadp_1_km(sp, razr, dat, prov, norm, m_eksp, norm_k,nach_km)
    sp = vstavit_shapku(sp, tk, km,nach_km-1)

    sp = vstavit_osn_nadp(sp, nach_km-1)
    sp = prostavit_num_strok(sp, nach_km+14,37,nach_km+75,63)
    sp = prostavit_num_stranic(sp, nach_km-1)
    return sp

def shapka1_km(sp,spisok_tk):
    nnomer_dse, nazv_dse = [x for x in spisok_tk[0][0].split('$')]
    n_tk, km, es = [x for x in spisok_tk[1][0].split('/')]
    sp.append(F.vpis("ГОСТ 3.1118-82  ФОРМА 4  САПР  ", 65, ' ', ' ', 2))
    sp.append(F.vpis("-" * 63, 65))
    sp.append(':          :                ' + F.vpis(n_tk, 25) + '     :     :')
    sp.append(F.vpis("-" * 63, 65))
    sp.append(F.vpis("", 5, prz=' ') + F.vpis(nnomer_dse, 24) + 13 * " " + F.vpis(km, 23))
    sp.append(F.vpis("", 5, prz=' ') + F.vpis("", 24) + 13 * " " + F.vpis("", 23))
    sp.append(F.vpis("-" * 63, 65))
    sp.append(
        ':    ' + F.vpis(nazv_dse, 48) + F.vpis(spisok_tk[2], 5, '',
                                                                                                ':') + '   :   :')
    sp.append(F.vpis("-" * 63, 65))
    sp.append(':__В_:ЦЕХ:__УЧ._:_РМ:ОПЕР:______КОД,_НАИМЕНОВАНИЕ_ОПЕРАЦИИ______:')
    sp.append(':__Г_:__________________ОБОЗНАЧЕНИЕ__ДОКУМЕНТА__________________:')
    sp.append(':__Д_:______________КОД,_НАИМЕНОВАНИЕ ОБОРУДОВАНИЯ______________:')
    sp.append(':__Е_:_СМ:_ПРОФ.:_Р_:_УТ_:_КР:КОИД:_ЕН_:_ОП_:КШТ.:_Т_ПЗ_:_Т_ШТ._:')
    sp.append(':_Л/М:______НАИМЕНОВАНИЕ ДЕТАЛИ, СБ. ЕДИНИЦЫ_ИЛИ_МАТЕРИАЛА______:')
    sp.append(':_Н/М:______ОБОЗНАЧЕНИЕ, КОД______:_ОПП:_ЕВ_:_ЕН_:__КИ__:Н.РАСХ.:')
    return sp


def prostavit_num_stranic(sp,nach=0):
    if (len(sp)-nach) % 63 == 0:
        n = int((len(sp)-nach) / 63)
    else:
        n = int(round((len(sp)-nach) / 63))
    if n == 1:
        sp[2+nach] = ':          :                      :                 :     :  1  :'
    else:
        sp[2+nach] = ':          :                      :                 ' + F.vpis(str(n), 7) + '  1  :'
        n = 2
        for i in range(65+nach, len(sp), 63):
            sp[i] = ':                :                      :                 ' + F.vpis(str(n), 7)
            n += 1
    return sp


def prostavit_num_strok(sp,nach1,dlina1,nach2,shag):

    n = 1
    for i in range(nach1, dlina1+nach1):
        obr = " " * (2 - len(str(n))) + str(n)
        sp[i] = sp[i][:3] + obr + sp[i][5:]
        n += 1
    for j in range(nach2, len(sp), shag):
        n = 1
        for i in range(j, j + 43):
            obr = " " * (2 - len(str(n))) + str(n)
            sp[i] = sp[i][:3] + obr + sp[i][5:]
            n += 1
    return sp


def vstavit_osn_nadp(sp, nach = 0):
    flag = False
    i = 118 + nach
    while flag == False:
        if i >= len(sp) - 1:
            break
        sp.insert(i + 1, F.vpis("-" * 63, 65))
        sp.insert(i + 2, ': :   :   :        :             :   :   :        :             :')
        sp.insert(i + 3, F.vpis("-" * 63, 65))
        sp.insert(i + 4, ':Подл:       :            :Взам:       :Дубл:       :           :')
        sp.insert(i + 5, F.vpis("-" * 63, 65))
        sp.insert(i + 6, ':  МК    :                                   :      :     :     :')
        sp.insert(i + 7, F.vpis("-" * 63, 65))
        i += 63
        if i >= len(sp) - 1:
            flag = True
    if len(sp) % 63 > 0:
        for i in range(0, 63 - len(sp) % 63 - 7):
            sp.append(':    ' + F.vpis(" " * 58, 60))
        sp.append(F.vpis("-" * 63, 65))
        sp.append(': :   :   :        :             :   :   :        :             :')
        sp.append(F.vpis("-" * 63, 65))
        sp.append(':Подл:       :            :Взам:       :Дубл:       :           :')
        sp.append(F.vpis("-" * 63, 65))
        sp.append(':  МК    :                                   :      :     :     :')
        sp.append(F.vpis("-" * 63, 65))
    return sp


def vstavit_shapku(sp, n_dse, n_tk, nach=0):
    flag = False
    i = nach+62
    while flag == False:
        if i >= len(sp) - 1:
            break
        sp.insert(i + 1, F.vpis("ГОСТ 3.1118-82  ФОРМА 3Б  САПР  ", 65, ' ', ' ', 2))
        sp.insert(i + 2, F.vpis("-" * 63, 65))
        sp.insert(i + 3,
                  F.vpis(" " * 15, 16, ":", " ") + F.vpis(" " * 21, 23, ":", " ") + F.vpis(" " * 16, 18, ":", " ")
                  + F.vpis(" " * 5, 7))
        sp.insert(i + 4, F.vpis("-" * 63, 65))
        sp.insert(i + 5, F.vpis(" ", 5, ":", " ") + F.vpis(" ", 14, ":", " ") + F.vpis(n_dse, 23, ":", " ")
                  + F.vpis(n_tk, 23))
        sp.insert(i + 6, F.vpis(" ", 5, ":", " ") + F.vpis(" ", 14, ":", " ") + F.vpis(" ", 23, ":", " ")
                  + F.vpis(" ", 23))
        sp.insert(i + 7, F.vpis("-" * 63, 65))
        sp.insert(i + 8, ':__В_:ЦЕХ:__УЧ._:_РМ:ОПЕР:______КОД,_НАИМЕНОВАНИЕ_ОПЕРАЦИИ______:')
        sp.insert(i + 9, ':__Г_:__________________ОБОЗНАЧЕНИЕ__ДОКУМЕНТА__________________:')
        sp.insert(i + 10, ':__Д_:______________КОД,_НАИМЕНОВАНИЕ ОБОРУДОВАНИЯ______________:')
        sp.insert(i + 11, ':__Е_:_СМ:_ПРОФ.:_Р_:_УТ_:_КР:КОИД:_ЕН_:_ОП_:КШТ.:_Т_ПЗ_:_Т_ШТ._:')
        sp.insert(i + 12, ':_Л/М:______НАИМЕНОВАНИЕ ДЕТАЛИ, СБ. ЕДИНИЦЫ_ИЛИ_МАТЕРИАЛА______:')
        sp.insert(i + 13, ':_Н/М:______ОБОЗНАЧЕНИЕ, КОД______:_ОПП:_ЕВ_:_ЕН_:__КИ__:Н.РАСХ.:')
        i += 56
        if i >= len(sp) - 1:
            flag = True
    return sp

def vstavit_osn_nadp_1_km(sp, razr, dat, prov, norm, m_eksp, norm_k,nach_km):
    if len(sp)-nach_km < 51:
        for i in range(len(sp)-nach_km, 51):
            sp.append(':    ' + F.vpis(" " * 58, 60))
    i = nach_km + 50
    sp.insert(i + 1, F.vpis("-" * 63, 65))
    sp.insert(i + 2, F.vpis(" " * 3, 5) + F.vpis(" " * 1, 3, " ", " ") + F.vpis(" " * 8, 10) +
              F.vpis(" " * 4, 6, " ", " ") + F.vpis("Разраб.", 10, orient=0) +
              F.vpis(razr[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(dat, 12, ":", ":"))
    sp.insert(i + 3, F.vpis(" " * 3, 5) + F.vpis(" " * 1, 3, " ", " ") + F.vpis(" " * 8, 10) +
              F.vpis(" " * 4, 6, " ", " ") + F.vpis("Провер.", 10, orient=0) +
              F.vpis(prov[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":",
                                                                                                ":"))
    sp.insert(i + 4, F.vpis("-" * 22, 24, ":", "-") + F.vpis("М.норм.", 10, orient=0) +
              F.vpis("          ", 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":",
                                                                                                ":"))
    sp.insert(i + 5, F.vpis(" " * 22, 24, ":", " ") + F.vpis("      ", 10, orient=0) +
              F.vpis("          ", 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":",
                                                                                                  ":"))
    sp.insert(i + 6, F.vpis(" " * 22, 24, ":", " ") + F.vpis("Н.контр.", 10, orient=0) +
              F.vpis(norm_k[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":",
                                                                                                  ":"))
    sp.insert(i + 7, F.vpis("-" * 63, 65))
    sp.insert(i + 8, ':Подл:       :            :Взам:       :Дубл:       :           :')
    sp.insert(i + 9, F.vpis("-" * 63, 65))
    sp.insert(i + 10, ':  МК    :                                   :      :     :     :')
    sp.insert(i + 11, F.vpis("-" * 63, 65))
    return sp

def vstavit_osn_nadp_1( sp, razr, dat, prov, norm, m_eksp, norm_k):
    if len(sp) < 51:
        for i in range(len(sp), 52):
            sp.append(':    ' + F.vpis(" " * 58, 60))

    i = 51
    sp.insert(i + 1, F.vpis("-" * 63, 65))
    sp.insert(i + 2, F.vpis(" " * 3, 5) + F.vpis(" " * 1, 3, " ", " ") + F.vpis(" " * 8, 10) +
              F.vpis(" " * 4, 6, " ", " ") + F.vpis("Разраб.", 10, orient=0) +
              F.vpis(razr[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(dat, 12, ":", ":"))
    sp.insert(i + 3, F.vpis(" " * 3, 5) + F.vpis(" " * 1, 3, " ", " ") + F.vpis(" " * 8, 10) +
              F.vpis(" " * 4, 6, " ", " ") + F.vpis("Провер.", 10, orient=0) +
              F.vpis(prov[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":", ":"))
    sp.insert(i + 4, F.vpis("-" * 22, 24, ":", "-") + F.vpis("Нормир.", 10, orient=0) +
              F.vpis(norm[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":",
                                                                                                ":"))
    sp.insert(i + 5, F.vpis(" " * 22, 24, ":", " ") + F.vpis("М.эксп.", 10, orient=0) +
              F.vpis(m_eksp[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":",
                                                                                                  ":"))
    sp.insert(i + 6, F.vpis(" " * 22, 24, ":", " ") + F.vpis("Н.контр.", 10, orient=0) +
              F.vpis(norm_k[:10], 13, ' ', ' ', orient=0) + F.vpis(" " * 4, 6, ':', " ") + F.vpis(" " * 8, 12, ":",
                                                                                                  ":"))
    sp.insert(i + 7, F.vpis("-" * 63, 65))
    sp.insert(i + 8, ':Подл:       :            :Взам:       :Дубл:       :           :')
    sp.insert(i + 9, F.vpis("-" * 63, 65))
    sp.insert(i + 10, ':  МК    :                                   :      :     :     :')
    sp.insert(i + 11, F.vpis("-" * 63, 65))
    return sp


def obrezat_stroki( sp, dlina):
    flag = False
    i = 0
    while flag == False:
        if len(sp[i]) > dlina and sp[i][1] != ' ':
            kod = sp[i][1]
            nach = sp[i][0:5]
            stroka_l = sp[i][7:dlina - 7]
            stroka = sp[i][7:-1].split(' ')

            arr_stroka_l = stroka_l.split(' ')
            arr_stroka_l.pop()

            stroka_p = stroka[len(arr_stroka_l):]
            stroka_p_new = ' '.join(stroka_p)

            stroka_l_new = ' '.join(arr_stroka_l)
            sp[i] = nach + F.vpis(" " + stroka_l_new, dlina - 5, orient=0)
            sp.insert(i + 1, ':' + kod + '   ' + F.vpis(" " + stroka_p_new, dlina - 5, orient=0))
        if i == len(sp) - 1:
            flag = True
        i += 1
    return sp


def vivod_telo_1( sp_b, tip, sp='', p1='', p2='', p3='', p4='', p5='', p6='', p7='', p8='', p9='', prop=1):
    if type(sp) == type([]) and sp[0] == "":
        return sp_b
    for i in range(0, prop):
        sp_b.append(':    ' + F.vpis(" " * 58, 60))
    if tip == 'Д':
        for i in sp:
            sp_b.append(':Д   ' + F.vpis(" " + i, 60, orient=0))
    if tip == 'В':
        sp_b.append(':В   ' + F.vpis(" " + p1, 12, ":", " ", orient=0) + ' ' * 3 + F.vpis(p2, 6, " ", " ", orient=0)
                    + F.vpis(p3, 39, " ", orient=0))
    if tip == 'Г':
        sp_b.append(':Г   ' + F.vpis(" " + p1, 60, orient=0))

    if tip == 'Е':
        sp_b.append(':Е   ' + F.vpis(' ', 4, ":", " ", orient=2) + F.vpis(p1, 8, " ", " ") + F.vpis(" ", 8, " ", " ") +
                    F.vpis(p2, 5, " ", " ") + F.vpis(p3, 5, " ", " ") + F.vpis(p4, 5, " ", " ") + F.vpis(" ", 5, " ",
                                                                                                         " ")
                    + F.vpis(" ", 5, " ", " ") + F.vpis(p5, 7, " ", " ") + F.vpis(p6, 8, " ", ":"))
        #:__Е_:_СМ:_ПРОФ.:_Р_:_УТ_:_КР:КОИД:_ЕН_:_ОП_:КШТ.:_Т_ПЗ_:_Т_ШТ._:
        #:Е 11:     588    2  20 2  1      1    1       0.20000   0.00666:
    if tip == 'О':
        sp_b.append(':О   ' + F.vpis(" " + p1, 60, orient=0))
    if tip == 'Т':
        for i in sp:
            sp_b.append(':Т   ' + F.vpis(" " + i, 60, orient=0))
    if tip == 'М':
        for i in sp:
            sp_b.append(':    ' + F.vpis(" " * 58, 60))
            kod, naim, ed,norm = [x for x in i.split("$")]
            sp_b.append(':M   ' + F.vpis(" " + naim, 60, orient=0))
            sp_b.append(':M   ' + F.vpis(" " + kod, 30,":"," ", orient=0) + F.vpis(ed, 14," "," ")
                                                                        + F.vpis(norm, 16," ",":",orient=2))
    return sp_b
