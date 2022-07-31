from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWinExtras import QtWin
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStyle
import os
import random
# import subprocess
import Cust_Qt as CQT
CQT.conver_ui_v_py()

from mydesign import Ui_MainW  # импорт нашего сгенерированного файла
from mydesign2 import Ui_Dialog  # импорт нашего сгенерированного файла

import Cust_SQLite as CSQ
import sys
import Cust_Functions as F
from GOST3111882F3 import vigruzit2 as GF3
import Cust_mes as CMS
from pathlib import Path
import operacii

import hashlib
import osn_materials as osn_mat
import nomenklatura as nomen_erp
# import proizv_calendar# Проверка производственного календаря...
import Cust_dxf as CDXF


'''
ТК 
0 Название техкарты , 1-отметка о прикреплении ... , 2- номер ТК, 3-сводный код, 4-, 5-Дата, 6-ФИО разработал , 7- примечание  .... 
13 - документ карты ($), , 14- параметрика($) , 15- Документ, 20 - уровень

Опер
0-Название оп, 1 - отметка документа ... , 2-номер операции, 3-сводный код, 4- рабочий центр код, 5-Оборудование, 6-Тпз, 7 - Тшт, 
8 -Профессия, 9 - КР , 10 - маетриалы (kod$naim$ed$norma{kod$naim$ed$norma), 11 - КОИД , 12 - , 13 - документы($ op), 14- параметрика($), 20 - уровень

переход
0 - название перехода, 1-отметка о прикреплении ... , 2- номер ТК, 3-сводный код, 4- номер чего то, 7 - Тшт, 11 - приспособления ($)
12 - инструмент ($), 13 - документы($ op), 14- параметрика($), ... 20 - уровень
'''

def db_files_create():
    print("Проверка наличия БД файлов...")
    put_bd = F.scfg('add_docs') + F.sep() + 'files.db'
    if F.nalich_file(put_bd):
        print("   Найдена.")
    else:
        frase = '''CREATE TABLE IF NOT EXISTS reestr(
       Пномер INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE ON CONFLICT ROLLBACK,
       size INTEGER,
       hesh TEXT,
       name TEXT,
       rashir TEXT,
       teh_karts TEXT,
       file TEXT);
        '''
        CSQ.sozd_bd_sql(put_bd,frase)
        print("    Создана")
        conn, cur = CSQ.connect_bd(put_bd)
        spis_filov = F.spis_files(F.scfg('add_docs'))
        for file in spis_filov[0][2]:
            rashir = file.split('.')[-1]
            if file != 'files.db' and rashir != 'pickle':
                size = os.path.getsize(F.scfg('add_docs') + os.sep + file)
                bin_file = F.convert_to_binary_data(F.scfg('add_docs') + os.sep + file)
                hesh = hashlib.sha1(bin_file).hexdigest()
                name = file
                #zapros = f"""
                #                        SELECT * FROM reestr WHERE size == '{size}' and hesh == '{hesh}'"""
                #query = CSQ.zapros(put_bd, zapros, conn)
                #if len(query) == 1:
                CSQ.dob_strok_v_bd_sql(put_bd, 'reestr', [[size, hesh, name, rashir,'', bin_file]], conn=conn)
                print(f'Добавлен {name}')
        CSQ.close_bd(conn)


def db_files_nalich(put_file,nom_tk):
    file = put_file.split(os.sep)[-1]
    put_bd = F.scfg('add_docs') + F.sep() + 'files.db'
    rashir = file.split('.')[-1]
    size = os.path.getsize(put_file)
    bin_file = F.convert_to_binary_data(put_file)
    hesh = hashlib.sha1(bin_file).hexdigest()
    name = file
    conn, cur = CSQ.connect_bd(put_bd)
    zapros = f"""
                                            SELECT * FROM reestr WHERE size == '{size}' and hesh == '{hesh}'"""
    query = CSQ.zapros(put_bd, zapros, conn)
    if len(query) == 1:
        CSQ.dob_strok_v_bd_sql(put_bd, 'reestr', [[size, hesh, name, rashir, nom_tk, bin_file]], conn=conn)
        query = CSQ.zapros(put_bd, zapros, conn)
    else:
        nk_tk = F.nom_kol_po_im_v_shap(query,'teh_karts')
        nk_pn = F.nom_kol_po_im_v_shap(query, 'Пномер')
        nom_tk_new = ''
        if query[1][nk_tk] != '':
            nom_tk_old = query[1][nk_tk].split('|')
            if nom_tk not in nom_tk_old:
                nom_tk_old.append(nom_tk)
                nom_tk_new = '|'.join(nom_tk_old)
        else:
            nom_tk_new = nom_tk
        if nom_tk_new != '':
            pn = query[1][nk_pn]
            frase = f'''
                            UPDATE reestr SET teh_karts = '{nom_tk_new}' WHERE Пномер = {pn}'''
            CSQ.zapros(put_bd,frase,conn)
    CSQ.close_bd(conn)
    nk_name = F.nom_kol_po_im_v_shap(query,'name')
    return query[1][nk_name]

def db_files_load(name):
    put_bd = F.scfg('add_docs') + F.sep() + 'files.db'
    conn, cur = CSQ.connect_bd(put_bd)
    zapros = f"""
                                                SELECT * FROM reestr WHERE name == '{name}'"""
    query = CSQ.zapros(put_bd, zapros, conn)
    CSQ.close_bd(conn)
    if len(query) == 1:
        return False
    nk_name = F.nom_kol_po_im_v_shap(query, 'name')
    nk_bin_file = F.nom_kol_po_im_v_shap(query, 'file')
    #return query[1][nk_name]
    put_tmp = CMS.tmp_dir() + os.sep + 'tmp_files'
    if F.nalich_file(put_tmp):
        F.ochist_papky(put_tmp)
    else:
        F.sozd_dir(put_tmp)
    put_file_tmp = CMS.tmp_dir() + os.sep + 'tmp_files' + os.sep + \
                   str(F.time_metka()).split('.')[-1] + "_" +\
                   F.transliterate(query[1][nk_name].replace('ь', ''))
    F.write_to_file(query[1][nk_bin_file],put_file_tmp)
    return put_file_tmp

def db_files_del(put_file,nom_tk):
    put_bd = F.scfg('add_docs') + F.sep() + 'files.db'
    conn, cur = CSQ.connect_bd(put_bd)
    zapros = f"""
                                            SELECT * FROM reestr WHERE name == '{put_file}'"""
    query = CSQ.zapros(put_bd, zapros, conn)
    if len(query) == 1:
        return False
    else:
        nk_tk = F.nom_kol_po_im_v_shap(query,'teh_karts')
        nk_pn = F.nom_kol_po_im_v_shap(query, 'Пномер')
        nom_tk_new = ''
        if query[1][nk_tk] != '':
            nom_tk_old = query[1][nk_tk].split('|')
            if nom_tk in nom_tk_old:
                nom_tk_old.remove(nom_tk)
            nom_tk_new = '|'.join(nom_tk_old)

        if nom_tk_new != '':
            pn = query[1][nk_pn]
            frase = f'''
                            UPDATE reestr SET teh_karts = '{nom_tk_new}' WHERE Пномер = {pn}'''
            CSQ.zapros(put_bd,frase,conn)
        else:
            pn = query[1][nk_pn]
            frase = f'''
                                        DELETE FROM reestr WHERE Пномер = {pn}'''
            CSQ.zapros(put_bd, frase, conn)
    CSQ.close_bd(conn)
    nk_name = F.nom_kol_po_im_v_shap(query,'name')
    return query[1][nk_name]


class mywindow2(QtWidgets.QDialog):  # диалоговое окно
    def __init__(self, parent=None, item_o="", p1=0, p2=0):
        self.item_o = item_o
        self.p1 = p1
        self.p2 = p2
        self.myparent = parent
        super(mywindow2, self).__init__()
        self.ui2 = Ui_Dialog()
        self.ui2.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle("Технологические карты")
        self.PUT_K_TMP = F.put_po_umolch() + os.sep + "tmptehkart"
        CQT.load_theme(self)
        combo1 = self.ui2.combo1
        combo2 = self.ui2.combo2
        combo1.setEnabled(False)
        combo2.setEnabled(False)
        combo1.setEditable(True)
        combo1.activated.connect(self.vibor_elem1)
        combo2.activated.connect(self.vibor_elem2)
        tab_v = self.ui2.tab_vib
        tab_v.doubleClicked.connect(self.vibor_iz_tab_vib_v_tableW_oper_mat)


        text = self.ui2.lineEdit
        text.setEnabled(False)
        tab = self.ui2.tab_vib
        tab.setEnabled(False)
        self.ui2.lbl_prim.setWordWrap(True)

        if self.item_o == "Док_оп" or self.item_o == "Док_тк":
            tab.setEnabled(True)
            if F.nalich_file(F.scfg('cash') + os.sep + "bd_docs.txt"):
                spisok = F.otkr_f(F.scfg('cash') + os.sep + "bd_docs.txt", False)
                spisok.insert(0, 'Код|Наименование|Комментарий')
                CQT.zapoln_wtabl(self, spisok, tab, isp_shapka=True, separ='|', ogr_maxshir_kol=800)
                self.setGeometry(self.frameGeometry().getCoords()[0], 33, self.width(), 1000)
                tab.setFocus()

        if self.item_o == "Профессия":
            tab.setEnabled(True)
            if F.nalich_file(F.scfg('cash') + os.sep + "bd_prof.txt"):
                spisok = F.otkr_f(F.scfg('cash') + os.sep + "bd_prof.txt", False)
                spisok.insert(0, 'Код|Наименование|Комментарий')
                CQT.zapoln_wtabl(self, spisok, tab, isp_shapka=True, separ='|', ogr_maxshir_kol=800)
                self.setGeometry(self.frameGeometry().getCoords()[0], 33, self.width(), 1000)
                tab.setFocus()

        if self.item_o == "Оборудование":
            tab.setEnabled(True)
            if F.nalich_file(F.scfg('cash') + os.sep + "bd_oborud.txt"):
                spisok = F.otkr_f(F.scfg('cash') + os.sep + "bd_oborud.txt", False)
                spisok.insert(0, 'Код|Наименование|Комментарий')
                CQT.zapoln_wtabl(self, spisok, tab, isp_shapka=True, separ='|', ogr_maxshir_kol=800)
                self.setGeometry(self.frameGeometry().getCoords()[0], 33, self.width(), 1000)
                tab.setFocus()

        if self.item_o == "Раб_ц":
            tab.setEnabled(True)
            if F.nalich_file(F.scfg('cash') + os.sep + "bd_rab_c.txt"):
                spisok = F.otkr_f(F.scfg('cash') + os.sep + "bd_rab_c.txt", False)
                spisok.insert(0, 'Код|Наименование|Комментарий')
                CQT.zapoln_wtabl(self, spisok, tab, isp_shapka=True, separ='|', ogr_maxshir_kol=800)
                self.setGeometry(self.frameGeometry().getCoords()[0], 33, self.width(), 1000)
                tab.setFocus()

        if item_o == "Материал":
            tab.setEnabled(True)
            put_nomen = F.scfg('cash') + F.sep() + 'nomenklatura_erp.db'
            if  F.nalich_file(put_nomen):
                conn, cur = CSQ.connect_bd(put_nomen)
            #if F.nalich_file(F.scfg('cash') + os.sep + "bd_mater.txt"):
            #    spisok = F.otkr_f(F.scfg('cash') + os.sep + "bd_mater.txt", False)
            #    #spisok.insert(0, 'Номер|Наименование|ед. изм.')
            #    CQT.zapoln_wtabl(self, spisok, tab, isp_shapka=True, separ='|', ogr_maxshir_kol=800)
                zapros = f'''SELECT DISTINCT Вид FROM nomen;'''
                rez = CSQ.zapros(put_nomen,zapros=zapros,shapka=False,conn=conn)
                if rez == None:
                    CQT.msgbox('Ошибка загрузки из БД')
                    return
                if len(rez) == 1:
                    CQT.msgbox('Ошибка загрузки из БД')
                    return
                rez.sort()
                for i in range(len(rez)):
                    combo1.addItem(rez[i][0])
                combo1.setEnabled(True)
                combo1.setEditable(False)
                combo1.setMaxVisibleItems(len(rez))
                combo1.setFocus()

                tab = self.ui2.tab_vib
                zapros = f'''SELECT * FROM nomen WHERE На_удаление == 0 ;'''
                rez = CSQ.zapros(put_nomen, zapros=zapros, shapka=True,conn=conn)
                CQT.zapoln_wtabl(self, rez, tab, isp_shapka=True, separ='', ogr_maxshir_kol=800)
                CMS.zapolnit_filtr(self, self.ui2.tbl_filtr, tab)
                CSQ.close_bd(conn)
            self.setGeometry(application.frameGeometry().getCoords()[0], application.frameGeometry().getCoords()[1], application.width(), application.height())

        if item_o == "Оснастка":
            combo1.setEnabled(True)
            if F.nalich_file(F.scfg('cash') + os.sep + "osnast.txt"):
                sp_vid_osn = F.otkr_f(F.scfg('cash') + os.sep + "osnast.txt", False)
                combo1.addItems(sp_vid_osn)
                self.vibor_elem1()
                text.setEnabled(True)
                combo1.setFocus()

        if item_o == "Инструмент":
            combo1.setEnabled(True)
            if F.nalich_file(F.scfg('cash') + os.sep + "instrum.txt"):
                sp_vid_ins = F.otkr_f(F.scfg('cash') + os.sep + "instrum.txt", False)
                combo1.addItems(sp_vid_ins)
                self.vibor_elem1()
                text.setEnabled(True)
                combo1.setFocus()

        if item_o == "Древо":
            text.setEnabled(True)
            if parent.currentItem() == None:
                return
            if parent.currentItem().text(20) == '0':
                limit = int(F.scfg('limit_k'))
                if F.nalich_file(F.scfg('cash') + os.sep + "kart.txt"):
                    strList = F.otkr_f(F.scfg('cash') + os.sep + "kart.txt", False, "|")
                    list_tmp = []
                    for item in strList:
                        if int(item[1]) > limit:
                            list_tmp.append(item[0])
                    completer = QtWidgets.QCompleter(list_tmp, parent=None)
                    text.setCompleter(completer)
                    combo2.setEnabled(True)
                    combo2.addItems(list_tmp)
                    combo2.setFocus()

            if parent.currentItem().text(20) == '1':
                limit = int(F.scfg('limit_o'))
                if F.nalich_file(F.scfg('cash') + os.sep + "oper.txt"):
                    strList = F.otkr_f(F.scfg('cash') + os.sep + "oper.txt", False, "|")
                    list_tmp = []
                    ind = 0
                    for i in range(len(strList)):
                        if int(strList[i][1]) > limit:
                            list_tmp.append(strList[i][0])
                            if strList[i][0] == text.text():
                                ind = i
                    completer = QtWidgets.QCompleter(list_tmp, parent=None)
                    text.setCompleter(completer)
                    combo2.setEnabled(True)
                    combo2.addItems(list_tmp)
                    combo2.setCurrentIndex(ind)
                    combo2.setFocus()
                    self.ui2.lbl_info_dxf.setText(str(application.global_param_tk_dxf))

            if parent.currentItem().text(20) == '2':
                ima_oper = parent.currentItem().parent().text(0)
                limit_o = int(F.scfg('limit_o'))
                limit = int(F.scfg('limit_p'))
                if F.nalich_file(F.scfg('cash') + os.sep + "oper.txt"):
                    strList = F.otkr_f(F.scfg('cash') + os.sep + "oper.txt", False, "|")
                    list_tmp = []
                    flag_naid = 0
                    for item in strList:
                        if item[0] == ima_oper and int(item[1]) > limit_o:
                            flag_naid = 1
                            break
                    if flag_naid == 1:
                        if F.nalich_file(F.scfg('cash') + os.sep + ima_oper + ".txt"):
                            strList = F.otkr_f(F.scfg('cash') + os.sep + ima_oper + ".txt", False, "|")
                            list_tmp = []
                            for item in strList:
                                if int(item[1]) > limit:
                                    list_tmp.append(item[0])
                    completer = QtWidgets.QCompleter(list_tmp, parent=None)
                    text.setCompleter(completer)
                    combo2.setEnabled(True)
                    combo2.addItems(list_tmp)
                    combo2.setFocus()
                    combo2.setCurrentText('')
        # ==========FILTR
        CMS.zapolnit_filtr(self, self.ui2.tbl_filtr, self.ui2.tab_vib)

    def vibor_iz_tab_vib_v_tableW_oper_mat(self):
        if self.item_o == "Материал":
            tab_v = self.ui2.tab_vib
            tab_mat = application.ui.tableW_oper_mat
            nk_db_nn = CQT.nom_kol_po_imen(tab_v, 'Код')
            nk_db_naim = CQT.nom_kol_po_imen(tab_v, 'Наименование')
            nk_db_edizm = CQT.nom_kol_po_imen(tab_v, 'ЕдиницаИзмерения')
            nk_tblm_nn = CQT.nom_kol_po_imen(tab_mat, 'Код')
            nk_tblm_naim = CQT.nom_kol_po_imen(tab_mat, 'Материал')
            nk_tblm_edizm = CQT.nom_kol_po_imen(tab_mat, 'Ед.Изм')
            nk_tblm_norma = CQT.nom_kol_po_imen(tab_mat, 'Норма')
            for i in range(0, tab_mat.columnCount()):
                if tab_mat.item(tab_mat.currentRow(), i) == None:
                    cellinfo = QtWidgets.QTableWidgetItem(tab_v.item(tab_v.currentRow(), i).text())
                    tab_mat.setItem(tab_mat.currentRow(), i, cellinfo)
            tab_mat.item(tab_mat.currentRow(), nk_tblm_nn).setText(
                tab_v.item(tab_v.currentRow(), nk_db_nn).text())
            tab_mat.item(tab_mat.currentRow(), nk_tblm_naim).setText(
                tab_v.item(tab_v.currentRow(), nk_db_naim).text())
            tab_mat.item(tab_mat.currentRow(), nk_tblm_edizm).setText(
                tab_v.item(tab_v.currentRow(), nk_db_edizm).text())
            tab_mat.item(tab_mat.currentRow(), nk_tblm_norma).setText(
                '0')
            self.hide()
            osn_mat.zagr_sortament(application)
            application.ui.tabW_mat.setCurrentIndex(1)
            application.ui.tbl_resch_mater.setFocus()
            if application.ui.tbl_resch_mater.item(0, 0) != None:
                application.ui.tbl_resch_mater.setCurrentCell(0, 0)

    def keyReleaseEvent(self, e):
        # print(str(int(e.modifiers())) + ' ' +  str(e.key()))
        if self.item_o == "Док_оп":
            tab_v = self.ui2.tab_vib
            if tab_v.hasFocus() == False:
                return
            if e.key() == 16777220:
                tab_doc = application.ui.tab_op_doc
                if tab_doc.item(tab_doc.currentRow(), 0) != None:
                    tab_doc.item(tab_doc.currentRow(), 0).setText(tab_v.item(tab_v.currentRow(), 0).text())
                else:
                    cellinfo = QtWidgets.QTableWidgetItem(tab_v.item(tab_v.currentRow(), 0).text())
                    tab_doc.setItem(tab_doc.currentRow(), 0, cellinfo)
                self.hide()
        if self.item_o == "Док_тк":
            tab_v = self.ui2.tab_vib
            if tab_v.hasFocus() == False:
                return
            if e.key() == 16777220:
                tab_doc = application.ui.tab_tk_doc
                if tab_doc.item(tab_doc.currentRow(), 0) != None:
                    tab_doc.item(tab_doc.currentRow(), 0).setText(tab_v.item(tab_v.currentRow(), 0).text())
                else:
                    cellinfo = QtWidgets.QTableWidgetItem(tab_v.item(tab_v.currentRow(), 0).text())
                    tab_doc.setItem(tab_doc.currentRow(), 0, cellinfo)
                self.hide()
        if self.item_o == "Профессия":
            tab_v = self.ui2.tab_vib
            if tab_v.hasFocus() == False:
                return
            if e.key() == 16777220:
                tab_op = application.ui.tab_op
                if tab_op.item(tab_op.currentRow(), 7) != None:
                    tab_op.item(tab_op.currentRow(), 7).setText(tab_v.item(tab_v.currentRow(), 0).text())
                else:
                    cellinfo = QtWidgets.QTableWidgetItem(tab_v.item(tab_v.currentRow(), 0).text())
                    tab_op.setItem(tab_op.currentRow(), 7, cellinfo)
                self.hide()
        if self.item_o == "Оборудование":
            tab_v = self.ui2.tab_vib
            if tab_v.hasFocus() == False:
                return
            if e.key() == 16777220:
                tab_op = application.ui.tab_op
                if tab_op.item(tab_op.currentRow(), 4) != None:
                    tab_op.item(tab_op.currentRow(), 4).setText(tab_v.item(tab_v.currentRow(), 1).text())
                else:
                    cellinfo = QtWidgets.QTableWidgetItem(tab_v.item(tab_v.currentRow(), 1).text())
                    tab_op.setItem(tab_op.currentRow(), 4, cellinfo)
                self.hide()
        if self.item_o == "Раб_ц":
            tab_v = self.ui2.tab_vib
            if tab_v.hasFocus() == False:
                return
            if e.key() == 16777220:
                tab_op = application.ui.tab_op
                if tab_op.item(tab_op.currentRow(), 3) != None:
                    tab_op.item(tab_op.currentRow(), 3).setText(tab_v.item(tab_v.currentRow(), 0).text())
                else:
                    cellinfo = QtWidgets.QTableWidgetItem(tab_v.item(tab_v.currentRow(), 0).text())
                    tab_op.setItem(tab_op.currentRow(), 3, cellinfo)
                self.hide()
        if self.item_o == "Материал":
            tab_v = self.ui2.tab_vib
            if tab_v.hasFocus():
                if e.key() == 16777220:
                    self.vibor_iz_tab_vib_v_tableW_oper_mat()
            if self.ui2.tbl_filtr.hasFocus():
                if e.key() == 16777220:
                    CMS.primenit_filtr(self, self.ui2.tbl_filtr, tab_v)

        if e.modifiers() == QtCore.Qt.ControlModifier:
            if e.key() == 83:
                if self.ui2.tab_vib.isEnabled():
                    self.ui2.tab_vib.setFocus(True)
            if e.key() == 87:
                self.ui2.lineEdit.setFocus(True)

        if self.ui2.lineEdit.text().strip() == "":
            return
        if len(self.ui2.lineEdit.text().strip()) < 4:
            return
        if self.ui2.lineEdit.hasFocus() == False:
            return

        if self.item_o == "Оснастка" or self.item_o == "Инструмент":

            if e.key() == 16777220:  # and int(e.modifiers()) == 67108864:
                combo1 = self.ui2.combo1
                combo2 = self.ui2.combo2
                if combo1.currentText() == '':
                    combo1.setFocus(True)
                    CQT.msgbox('Не выбрана категория')
                    return
                print("Нажата клавиша <Enter>")
                cu = self.myparent
                strok = self.ui2.lineEdit.text().strip().replace('\n', ' ')
                strok = F.ochist_strok_pod_separ(strok)
                strok = F.zaglav_bukva(strok)
                self.hide()
                cellinfo = QtWidgets.QTableWidgetItem(strok)
                cu.setItem(cu.currentRow(), 0, cellinfo)
                cu.item(self.p1, 0).setText(strok)
                if self.item_o == "Оснастка":
                    if F.nalich_file(F.scfg('cash') + os.sep + "osnast.txt"):
                        arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + "osnast.txt")
                        flag_naid = 0
                        for item_arr in arr_tmp:
                            if item_arr == combo1.currentText():
                                flag_naid = 1
                                break
                        if flag_naid == 0:
                            arr_tmp.append(combo1.currentText())
                        F.zap_f(F.scfg('cash') + os.sep + "osnast.txt", arr_tmp)
                    else:
                        arr_tmp = []
                        arr_tmp.append(combo1.currentText())
                        F.zap_f(F.scfg('cash') + os.sep + "osnast.txt", arr_tmp)
                    if F.nalich_file(F.scfg('cash') + os.sep + "osn_" + combo1.currentText() + ".txt"):
                        arr_osn = F.otkr_f(F.scfg('cash') + os.sep + "osn_" + combo1.currentText() + ".txt")
                        flag_naid = 0
                        for item_arr in arr_osn:
                            if item_arr == strok:
                                flag_naid = 1
                                break
                        if flag_naid == 0:
                            arr_osn.append(strok)
                        F.zap_f(F.scfg('cash') + os.sep + "osn_" + combo1.currentText() + ".txt", arr_osn)
                    else:
                        arr_osn = []
                        arr_osn.append(strok)
                        F.zap_f(F.scfg('cash') + os.sep + "osn_" + combo1.currentText() + ".txt", arr_osn)
                if self.item_o == "Инструмент":
                    if F.nalich_file(F.scfg('cash') + os.sep + "instrum.txt"):
                        arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + "instrum.txt")
                        flag_naid = 0
                        for item_arr in arr_tmp:
                            if item_arr == combo1.currentText():
                                flag_naid = 1
                                break
                        if flag_naid == 0:
                            arr_tmp.append(combo1.currentText())
                        F.zap_f(F.scfg('cash') + os.sep + "instrum.txt", arr_tmp)
                    else:
                        arr_tmp = []
                        arr_tmp.append(combo1.currentText())
                        F.zap_f(F.scfg('cash') + os.sep + "instrum.txt", arr_tmp)
                    if F.nalich_file(F.scfg('cash') + os.sep + "ins_" + combo1.currentText() + ".txt"):
                        arr_ins = F.otkr_f(F.scfg('cash') + os.sep + "ins_" + combo1.currentText() + ".txt")
                        flag_naid = 0
                        for item_arr in arr_ins:
                            if item_arr == strok:
                                flag_naid = 1
                                break
                        if flag_naid == 0:
                            arr_ins.append(strok)
                        F.zap_f(F.scfg('cash') + os.sep + "ins_" + combo1.currentText() + ".txt", arr_ins)
                    else:
                        arr_ins = []
                        arr_ins.append(strok)
                        F.zap_f(F.scfg('cash') + os.sep + "ins_" + combo1.currentText() + ".txt", arr_ins)

        if self.item_o == "Древо":
            if e.key() == 16777220:
                print("Нажата клавиша <Control Enter>tree")
                strok = self.ui2.lineEdit.text().strip().replace('\n', ' ')
                strok = F.ochist_strok_pod_separ(strok)
                strok = F.zaglav_bukva(strok)
                item = application.ui.tree.currentItem()
                if item == None:
                    return

                print(item.text(0))
                item.setText(0, strok)
                print(item.text(0))

                if item.text(20) == '0':
                    if F.nalich_file(F.scfg('cash') + os.sep + "kart.txt"):
                        arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + "kart.txt", False, "|")
                        flag_naid = 0
                        for item_arr in arr_tmp:
                            if item_arr[0] == strok:
                                item_arr[1] = str(int(item_arr[1]) + 1)
                                flag_naid = 1
                                break
                        if flag_naid == 0:
                            arr_tmp.append([strok, '1'])
                        F.zap_f(F.scfg('cash') + os.sep + "kart.txt", arr_tmp, "|")
                    else:
                        arr_tmp = []
                        arr_tmp.append([strok, '1'])
                        F.zap_f(F.scfg('cash') + os.sep + "kart.txt", arr_tmp, "|")

                if item.text(20) == '1':
                    item = mywindow.zagruzka_shablona_operacii(mywindow, item, self.PUT_K_TMP)
                    if F.nalich_file(F.scfg('cash') + os.sep + "oper.txt"):
                        arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + "oper.txt", False, "|")
                        set_oper = {_[0] for _ in arr_tmp}
                        if self.ui2.lineEdit.text() not in set_oper:
                            item.setText(0, 'ОШИБКА')
                            CQT.msgbox('Операция не в списке, проверяйся')
                            return
                        if self.kontrol_zapolnenia_peremennih():
                            item = self.raschet_tsht(item, self.ui2.tab_vib)
                            item = self.raschet_kompleksov(item, self.ui2.tab_vib)
                            application.obnovit_mater_tabl()
                        else:
                            CQT.msgbox('Контроль переменных не пройден, нормы не рассчитаны')
                        item.setText(6, str(self.tpz_na_operaciy(item.text(0), arr_tmp)))
                        flag_naid = 0
                        for item_arr in arr_tmp:
                            if item_arr[0] == strok:
                                item_arr[1] = str(int(item_arr[1]) + 1)
                                flag_naid = 1
                                break
                        if flag_naid == 0:
                            arr_tmp.append([strok, '1'])
                        F.zap_f(F.scfg('cash') + os.sep + "oper.txt", arr_tmp, "|")
                    else:
                        arr_tmp = []
                        arr_tmp.append([strok, '1'])
                        F.zap_f(F.scfg('cash') + os.sep + "oper.txt", arr_tmp, "|")

                if item.text(20) == '2':
                    oper = application.ui.tree.currentItem().parent().text(0)
                    limit_o = int(F.scfg('limit_o'))
                    limit_p = int(F.scfg('limit_p'))
                    if F.nalich_file(F.scfg('cash') + os.sep + "oper.txt"):
                        arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + "oper.txt", False, "|")
                        flag_naid = 0
                        for item_arr in arr_tmp:
                            if item_arr[0] == oper:
                                if int(item_arr[1]) > limit_p:
                                    flag_naid = 1
                                break
                        if flag_naid == 1:
                            if F.nalich_file(F.scfg('cash') + os.sep + oper + ".txt"):
                                arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + oper + ".txt", False, "|")
                                if self.kontrol_zapolnenia_peremennih():
                                    item = self.raschet_tsht(item, self.ui2.tab_vib)
                                    application.tree_noma_vrem()
                                    item = self.raschet_kompleksov(application.ui.tree.currentItem().parent(), self.ui2.tab_vib, True)
                                    application.obnovit_mater_tabl()
                                else:
                                    CQT.msgbox('Контроль переменных не пройден, нормы не рассчитаны')

                                flag_naid2 = 0
                                for item_arr in arr_tmp:
                                    if item_arr[0] == strok:
                                        item_arr[1] = str(int(item_arr[1]) + 1)
                                        flag_naid2 = 1
                                        break
                                if flag_naid2 == 0:
                                    arr_tmp.append([strok, '1'])
                                F.zap_f(F.scfg('cash') + os.sep + oper + ".txt", arr_tmp, "|")
                            else:
                                arr_tmp = []
                                arr_tmp.append([strok, '1'])
                                F.zap_f(F.scfg('cash') + os.sep + oper + ".txt", arr_tmp, "|")
                application.obnovit_param_tablic()
                self.hide()
        return

    def raschet_kompleksov(self, item, tbl, perehod = False):
        if perehod:
            ima_operacii = item.text(0)
            arr_tmp = ['',item.text(7).split('$')]
        else:
            ima_operacii = item.text(0)
            arr_tmp = CQT.spisok_iz_wtabl(tbl, shapka=True)
        try:
            mat = operacii.materiali(ima_operacii, arr_tmp)
        except:
            mat = ""
        if item.text(10) == '':
            old_spis_mat = []
        else:
            old_spis_mat = [x.split('$') for x in item.text(10).split('{')]
        new_spis_mat = [x.split('$') for x in mat.split('{')]
        for i in range(len(new_spis_mat)):
            flag_naid = False
            for j in range(len(old_spis_mat)):
                if new_spis_mat[i][0] == old_spis_mat[j][0]:
                    flag_naid = True
                    old_spis_mat[j] = new_spis_mat[i]
                    break
            if flag_naid == False:
                old_spis_mat.append(new_spis_mat[i])
        mat = '{'.join(['$'.join(strok) for strok in old_spis_mat if strok != ['']])

        item.setText(10, mat)
        return item

    def raschet_tsht(self, item, tbl):
        arr_tmp = CQT.spisok_iz_wtabl(tbl, shapka=True)
        if item.text(20) == '1':
            ima_operacii = item.text(0)
            try:
                vrema = operacii.vremya_tsht(ima_operacii, arr_tmp)
            except:
                vrema = 0
        if item.text(20) == '2':
            arr_tmp_parent = self.myparent.currentItem().parent().text(14).split("$")
            ima_operacii = self.myparent.currentItem().parent().text(0)
            ima_perehod = item.text(0)
            try:
                vrema = operacii.vremya_tsht_perehodi(ima_operacii,ima_perehod, arr_tmp, arr_tmp_parent)
            except:
                vrema = 0
        if vrema == 0:
            CQT.msgbox('Не рассчиано время, материалы не заненсены.')
        item.setText(7, str(vrema))
        item.setText(14, '$'.join(arr_tmp[-1]))
        return item

    def kontrol_zapolnenia_peremennih(self):
        tbl = self.ui2.tab_vib
        spis = CQT.spisok_iz_wtabl(tbl, shapka=True)
        if len(spis) != 2:
            return True
        for i in range(len(spis[0])):
            if spis[1][i] == "-":
                return False
            tip = spis[0][i].split(':')[-1].strip()
            if tip == 'int':
                if F.is_numeric(spis[1][i]) == False:
                    return False
        return True

    def vibor_elem1(self):
        combo1 = self.ui2.combo1
        combo2 = self.ui2.combo2
        text = self.ui2.lineEdit
        if self.item_o == "Оснастка":
            vid_osn = combo1.currentText()
            if F.nalich_file(F.scfg('cash') + os.sep + "osn_" + vid_osn + ".txt"):
                arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + "osn_" + vid_osn + ".txt")
                combo2.clear()
                combo2.setEnabled(True)
                combo2.addItems(arr_tmp)
            return
        if self.item_o == "Инструмент":
            vid_ins = combo1.currentText()
            if F.nalich_file(F.scfg('cash') + os.sep + "ins_" + vid_ins + ".txt"):
                arr_tmp = F.otkr_f(F.scfg('cash') + os.sep + "ins_" + vid_ins + ".txt")
                combo2.clear()
                combo2.setEnabled(True)
                combo2.addItems(arr_tmp)
            return
        if self.item_o == "Материал":
            vid = combo1.currentText()
            tab = self.ui2.tab_vib
            put_nomen = F.scfg('cash') + F.sep() + 'nomenklatura_erp.db'
            if F.nalich_file(put_nomen):
                zapros = f'''SELECT * FROM nomen WHERE Вид == "{vid}" AND На_удаление == 0 ;'''
                rez = CSQ.zapros(put_nomen, zapros=zapros, shapka=True)
                CQT.zapoln_wtabl(self, rez, tab, isp_shapka=True, separ='', ogr_maxshir_kol=800)
                CMS.zapolnit_filtr(self,self.ui2.tbl_filtr,tab)
            return

    def vibor_elem2(self):
        combo1 = self.ui2.combo1
        combo2 = self.ui2.combo2
        tbl = self.ui2.tab_vib
        text = self.ui2.lineEdit
        text.setText(combo2.currentText())
        if self.item_o == 'Инструмент' or self.item_o == 'Оснастка':
            return
        item = application.ui.tree.currentItem()
        if self.item_o == 'Древо':
            if item.text(20) == '1':
                if F.nalich_file(F.scfg('cash') + os.sep + "oper.txt"):
                    spis_op = F.otkr_f(F.scfg('cash') + os.sep + "oper.txt", False, "|")
                    rez = []
                    rez.append(self.spis_parametrov_na_operaciy(combo2.currentText(), spis_op))
                    if rez != [['']]:
                        self.ui2.tab_vib.setEnabled(True)
                        rez.append(['-' for _ in range(len(rez[0]))])
                        if item.text(14) != '':
                            spis_per_param = item.text(14).split('$')
                            try:
                                for j in range(len(spis_per_param)):
                                    rez[-1][j] = spis_per_param[j]
                            except:
                                pass

                        if application.global_param_tk_dxf != '':
                            for parametr in application.SPIS_PARAMETR_DXF:
                                for i in range(len(rez[0])):
                                    if parametr == rez[0][i].split(':')[0]:
                                        #if CQT.msgboxgYN(f'Загрузить {parametr} из dxf?'):
                                        param_val = ''
                                        if parametr == 'Периметр':
                                            param_val = application.global_param_tk_dxf['perimetr_elems_mm']
                                        if parametr == 'Врезы':
                                            param_val = application.global_param_tk_dxf['elems']
                                        if parametr == 'Площадь':
                                            param_val = application.global_param_tk_dxf['rect_area_mm2']
                                        rez[1][i] = param_val

                        if item.text(4) == '010101' and 'ЧПУ' in item.text(0):
                            segment_count = '?'
                            if item.child(0).text(0) != '':
                                if 'част' in item.child(0).text(0).lower() or \
                                    'егмент' in item.child(0).text(0).lower() or \
                                    'сектор' in item.child(0).text(0).lower():
                                    if F.is_numeric(item.child(0).text(0).split()[-1]):
                                        segment_count = int(item.child(0).text(0).split()[-1])
                            for i in range(len(rez[0])):
                                if 'Число сегментов' == rez[0][i].split(':')[0]:
                                    rez[1][i] = segment_count
                                    break


                        set_corr = set(range(len(rez[0])))
                        CQT.zapoln_wtabl(self, rez, tbl, separ='', isp_shapka=True, set_editeble_col_nomera=set_corr)
                        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + combo2.currentText() + F.sep() + 'prim.txt'
                        if F.nalich_file(putf):
                            prim = F.otkr_f(putf, True, propuski=True)
                            prim = '; '.join([F.ochist_strok_pod_separ(x.strip()) for x in prim])
                            self.ui2.lbl_prim.setText(prim)
                    else:
                        self.ui2.tab_vib.clear()
                        self.ui2.tab_vib.setRowCount(0)
                        self.ui2.tab_vib.setEnabled(False)

            if item.text(20) == '2':
                ima_oper = self.myparent.currentItem().parent().text(0)
                if F.nalich_file(F.scfg('cash') + os.sep + ima_oper + ".txt"):
                    spis_pereh = F.otkr_f(F.scfg('cash') + os.sep + ima_oper + ".txt", False, "|")
                    rez = []
                    rez.append(self.spis_parametrov_na_perehod(combo2.currentText(), spis_pereh))
                    if rez != [['']]:
                        self.ui2.tab_vib.setEnabled(True)
                        rez.append(['-' for _ in range(len(rez[0]))])
                        if item.text(14) != '':
                            spis_per_param = item.text(14).split('$')
                            for j in range(len(spis_per_param)):
                                rez[-1][j] = spis_per_param[j]

                        set_corr = set(range(len(rez[0])))
                        CQT.zapoln_wtabl(self, rez, tbl, separ='', isp_shapka=True, set_editeble_col_nomera=set_corr)
                        putf = F.scfg(
                            'cash') + F.sep() + "tables" + F.sep() + ima_oper + F.sep() + combo2.currentText() + F.sep() + 'prim.txt'
                        if F.nalich_file(putf):
                            prim = F.otkr_f(putf, True, propuski=True)
                            prim = '; '.join([F.ochist_strok_pod_separ(x.strip()) for x in prim])
                            self.ui2.lbl_prim.setText(prim)
                    else:
                        self.ui2.tab_vib.clear()
                        self.ui2.tab_vib.setRowCount(0)
                        self.ui2.tab_vib.setEnabled(False)

    def spis_parametrov_na_operaciy(self, oper: str, spis_op: list):
        rez = []
        for i in range(len(spis_op)):
            if spis_op[i][0] == oper and len(spis_op[i]) > 3:
                spis_per = spis_op[i][3].split(';')
                for j in range(len(spis_per)):
                    rez.append(spis_per[j])
        return rez

    def spis_parametrov_na_perehod(self, oper: str, spis_op: list):
        rez = []
        for i in range(len(spis_op)):
            if spis_op[i][0] == oper and len(spis_op[i]) > 2:
                spis_per = spis_op[i][2].split(';')
                for j in range(len(spis_per)):
                    rez.append(spis_per[j])
        return rez

    def tpz_na_operaciy(self, oper: str, spis_op: list):
        tpz = ''
        for i in range(len(spis_op)):
            if spis_op[i][0] == oper and len(spis_op[i]) > 2:
                if F.is_numeric(spis_op[i][2]):
                    return F.valm(spis_op[i][2])
        return tpz



class mywindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):

        super(mywindow, self).__init__()
        self.ui = Ui_MainW()
        self.ui.setupUi(self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowTitle("TexkartMakerElite")
        self.nom_tk = ''
        self.dse_nn = ''
        self.dse_naim = ''
        self.global_param_tk_dxf = ''
        self.SPIS_PARAMETR_DXF = ['Периметр','Врезы','Площадь']
        self.showMaximized()

        F.test_path()
        self.resized.connect(self.widths)

        self.flag_proverka_op = True

        self.PUT_K_TMP = F.put_po_umolch() + os.sep + "tmptehkart"

        CQT.load_theme(self)
        tree = self.ui.tree
        tree.setColumnCount(3)
        tree.headerItem().setText(0, QtCore.QCoreApplication.translate("MainW", "Элемент"))
        tree.headerItem().setText(1, QtCore.QCoreApplication.translate("MainW", "Документ"))
        tree.headerItem().setText(2, QtCore.QCoreApplication.translate("MainW", "№"))
        tree.setStyleSheet(
            "QTreeView {color: rgb(22, 33, 22); background-color: rgb(212, 212, 212);} QTreeView::item:hover {rgb(52, 63, 52); background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop:"
            " 0 #e7effd, stop: 1 #cbdaf1);border: 1px solid #bfcde4;} ")
        tree.setFocusPolicy(15)
        # tree.itemPressed.connect(self.obnovit_param_tablic)
        tree.doubleClicked.connect(self.spisok)
        tree.itemSelectionChanged.connect(self.obnovit_param_tablic)

        tabl = self.ui.tab_op
        shapka = ['ID', '№', 'Операция', 'Раб.центр', 'Оборудование', 'Тп.з.', 'Тшт.', 'Проф.', 'N раб.', 'КОИД']
        tabl.setColumnCount(10)
        tabl.setHorizontalHeaderLabels(shapka)
        tabl.verticalHeader().hide()
        tabl.horizontalHeader().setFixedHeight(29)
        tabl.cellChanged.connect(self.cvet_knopki)
        tabl.cellActivated.connect(self.cvet_knopki)
        CQT.ust_cvet_videl_tab(tabl)

        tab2 = self.ui.tap_per
        shapka = ['ID', '№', 'Тшт.']
        tab2.setColumnCount(3)
        tab2.setHorizontalHeaderLabels(shapka)
        tab2.horizontalHeader().setFixedHeight(29)
        tab2.verticalHeader().hide()
        tab2.cellChanged.connect(self.cvet_knopki)
        tab2.cellActivated.connect(self.cvet_knopki)
        CQT.ust_cvet_videl_tab(tab2)

        tab3 = self.ui.tab_kar
        shapka = ['ID', 'Изменен', 'Разработал', 'Примечание']
        tab3.setColumnCount(4)
        tab3.setHorizontalHeaderLabels(shapka)
        tab3.verticalHeader().hide()
        tab3.horizontalHeader().setFixedHeight(29)
        tab3.cellChanged.connect(self.cvet_knopki)
        tab3.cellActivated.connect(self.cvet_knopki)
        CQT.ust_cvet_videl_tab(tab3)

        tab_per_osn = self.ui.tap_per_osnast
        shapka = ['Оснастка']
        tab_per_osn.setColumnCount(1)
        tab_per_osn.setHorizontalHeaderLabels(shapka)
        tab_per_osn.verticalHeader().hide()
        tab_per_osn.setRowCount(9)
        tab_per_osn.horizontalHeader().setFixedHeight(22)
        tab_per_osn.cellChanged.connect(self.cvet_knopki)
        tab_per_osn.cellActivated.connect(self.cvet_knopki)

        tab_per_ins = self.ui.tap_per_insrt
        shapka = ['Инструмент']
        tab_per_ins.setColumnCount(1)
        tab_per_ins.setHorizontalHeaderLabels(shapka)
        tab_per_ins.verticalHeader().hide()
        tab_per_ins.setRowCount(9)
        tab_per_ins.horizontalHeader().setFixedHeight(22)
        tab_per_ins.cellChanged.connect(self.cvet_knopki)
        tab_per_ins.cellActivated.connect(self.cvet_knopki)

        tab_op_doc = self.ui.tab_op_doc
        shapka = ['Документы']
        tab_op_doc.setColumnCount(1)
        tab_op_doc.setHorizontalHeaderLabels(shapka)
        tab_op_doc.verticalHeader().hide()
        tab_op_doc.setRowCount(9)
        tab_op_doc.horizontalHeader().setFixedHeight(22)
        tab_op_doc.cellChanged.connect(self.cvet_knopki)
        tab_op_doc.cellActivated.connect(self.cvet_knopki)

        tab_tk_doc = self.ui.tab_tk_doc
        shapka = ['Документы']
        tab_tk_doc.setColumnCount(1)
        tab_tk_doc.setHorizontalHeaderLabels(shapka)
        tab_tk_doc.verticalHeader().hide()
        tab_tk_doc.setRowCount(9)
        tab_tk_doc.horizontalHeader().setFixedHeight(22)
        tab_tk_doc.cellChanged.connect(self.cvet_knopki)
        tab_tk_doc.cellActivated.connect(self.cvet_knopki)

        tab_mk = self.ui.tbl_isp_mk
        tab_mk.setSelectionBehavior(1)
        tab_mk.setSelectionMode(1)
        tab_mk.cellDoubleClicked[int, int].connect(self.zagruzit_old_tk)

        self.ui.tableW_oper_mat.clicked.connect(lambda _, x=self: osn_mat.zagr_sortament(x))

        tab_buf1 = self.ui.t_buff_1
        if F.nalich_file(self.PUT_K_TMP + os.sep + '1.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '1.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf1, 0, 0, (), (), 200, False, "|", 5)

        tab_buf2 = self.ui.t_buff_2
        if F.nalich_file(self.PUT_K_TMP + os.sep + '2.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '2.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf2, 0, 0, (), (), 200, False, "|", 5)

        tab_buf3 = self.ui.t_buff_3
        if F.nalich_file(self.PUT_K_TMP + os.sep + '3.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '3.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf3, 0, 0, (), (), 200, False, "|", 5)

        tab_buf4 = self.ui.t_buff_4
        if F.nalich_file(self.PUT_K_TMP + os.sep + '4.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '4.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf4, 0, 0, (), (), 200, False, "|", 5)

        tab_buf5 = self.ui.t_buff_5
        if F.nalich_file(self.PUT_K_TMP + os.sep + '5.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '5.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf5, 0, 0, (), (), 200, False, "|", 5)

        tab_buf6 = self.ui.t_buff_6
        if F.nalich_file(self.PUT_K_TMP + os.sep + '6.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '6.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf6, 0, 0, (), (), 200, False, "|", 5)

        tab_buf7 = self.ui.t_buff_7
        if F.nalich_file(self.PUT_K_TMP + os.sep + '7.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '7.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf7, 0, 0, (), (), 200, False, "|", 5)

        tab_buf8 = self.ui.t_buff_8
        if F.nalich_file(self.PUT_K_TMP + os.sep + '8.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '8.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf8, 0, 0, (), (), 200, False, "|", 5)

        tab_buf9 = self.ui.t_buff_9
        if F.nalich_file(self.PUT_K_TMP + os.sep + '9.txt'):
            spisok = F.otkr_f(self.PUT_K_TMP + os.sep + '9.txt')
            CQT.zapoln_wtabl(mywindow, spisok, tab_buf9, 0, 0, (), (), 200, False, "|", 5)

        self.ui.btn_mag_napolky.clicked.connect(self.magazin_na_polky)
        self.ui.btn_mag_sbros.clicked.connect(self.magazin_na_del)
        tbl_magaz = self.ui.tbl_magaz
        tbl_magaz.clicked.connect(self.tbl_magaz_click)
        self.ui.btn_mag_prim.clicked.connect(self.magazin_primenit)
        self.ui.btn_mag_up.clicked.connect(self.magazin_up)
        self.ui.btn_mag_down.clicked.connect(self.mag_down)
        tbl_magaz.setSelectionBehavior(1)
        tbl_magaz.setSelectionMode(1)
        CQT.ust_cvet_videl_tab(tbl_magaz)

        self.ui.btn_obnov_sp_mk.clicked.connect(self.nalichie_nevip_mk)

        butt_op = self.ui.Button_t_op
        butt_op.clicked.connect(self.obnovt_drevo_s_tabl1_op)

        butt_kar = self.ui.Button_t_kar
        butt_kar.clicked.connect(self.obnovt_drevo_s_tabl3_kar)

        butt_per = self.ui.Button_t_per
        butt_per.clicked.connect(self.obnovt_drevo_s_tab2_per)

        butt_sozd = self.ui.pushButton_sozd
        butt_sozd.clicked.connect(self.sozd_file)
        self.ui.pushButton_sozd.setEnabled(False)

        self.ui.tableW_oper_mat.clicked.connect(self.click_tableW_oper_mat)

        butt_mat = self.ui.Button_prim_mat
        butt_mat.clicked.connect(self.zap_mat_v_tree)

        butt_add_mat = self.ui.Button_create_mater
        butt_add_mat.clicked.connect(self.add_line_mat)

        butt_del_mat = self.ui.Button_del_mater
        butt_del_mat.clicked.connect(self.del_mat)

        butt_load_kod = self.ui.Button_load_kod
        butt_load_kod.clicked.connect(self.zagruz_mat_iz_nomenklatyri)


        butt_dob_doc = self.ui.pushButton_dob_doc
        butt_dob_doc.clicked.connect(self.dob_doc)

        butt_del_doc = self.ui.pushButton_del_doc
        butt_del_doc.clicked.connect(self.ydal_doc)

        butt_opn_doc = self.ui.pushButton_prosm_doc
        butt_opn_doc.clicked.connect(self.opn_doc)

        butt_up = self.ui.pushButton_Vverh
        butt_up.clicked.connect(self.tree_vverh)

        butt_down = self.ui.pushButton_Vniz
        butt_down.clicked.connect(self.tree_vniz)

        butt_copy = self.ui.pushButton_Copy
        butt_copy.clicked.connect(self.tree_copy)

        butt_paste = self.ui.pushButton_Paste
        butt_paste.clicked.connect(self.tree_paste)

        butt_del = self.ui.pushButton_Del
        butt_del.clicked.connect(self.tree_del)

        butt_vigruz = self.ui.pushButton_vigruzit
        butt_vigruz.clicked.connect(self.vigruzit)

        butt_otm_i_vihod = self.ui.pushButton_otm_i_vihod
        butt_otm_i_vihod.clicked.connect(self.otm_i_vihod)

        btn_vvod_rasch_mat = self.ui.btn_vvod_rez_mat
        btn_vvod_rasch_mat.clicked.connect(lambda _, x=self: osn_mat.vvod_rasch_mat(x))

        tab_oper_mat = self.ui.tbl_oper_mat
        tab_oper_mat.setSelectionBehavior(1)
        tab_oper_mat.clicked.connect(self.obnovit_mater_tabl)

        tab_oper_mat_red = self.ui.tableW_oper_mat
        shapka = ['Код', 'Материал', 'Ед.Изм', 'Норма']
        tab_oper_mat_red.setColumnCount(4)
        tab_oper_mat_red.setHorizontalHeaderLabels(shapka)

        tab = self.ui.tabW
        tab.currentChanged[int].connect(self.tab_click)

        tab_razr = self.ui.tabWidget
        tab_razr.currentChanged.connect(self.save_tk_vklad)

        self.ui.tabWidget.setTabEnabled(1, False)

        self.ui.comboBox_liter.addItems(F.otkr_f(F.tcfg('liter')))

        tabl_bd = self.ui.tblw_dse
        tabl_bd.clicked.connect(lambda _, x=False: self.vibor_dse(x))
        tabl_bd.cellChanged.connect(self.tex_zametki)
        tabl_bd.setSelectionBehavior(1)
        tabl_bd.setSelectionMode(1)




        btn_prim_izm_shablon = self.ui.btn_prim_shablon_op
        btn_prim_izm_shablon.clicked.connect(self.btn_prim_izm_shablon)

        btn_open_docs = self.ui.btn__open_docs
        btn_open_docs.clicked.connect(self.zapusk_docs)

        btn_status_process = self.ui.btn_process
        btn_status_process.clicked.connect(self.status_process)

        btn_status_normi = self.ui.btn_normi
        btn_status_normi.clicked.connect(self.status_normi)

        btn_status_mater = self.ui.btn_mater
        btn_status_mater.clicked.connect(self.status_mater)

        self.ui.opt_but_list.clicked.connect(lambda _, x=self: osn_mat.mat_list_load(x))
        self.ui.opt_but_krug.clicked.connect(lambda _, x=self: osn_mat.mat_krug_load(x))
        self.ui.opt_but_truba.clicked.connect(lambda _, x=self: osn_mat.mat_truba_load(x))
        self.ui.opt_but_ygol.clicked.connect(lambda _, x=self: osn_mat.mat_ygol_load(x))
        self.ui.opt_but_shvel.clicked.connect(lambda _, x=self: osn_mat.mat_shvel_load(x))
        self.ui.opt_but_dvut.clicked.connect(lambda _, x=self: osn_mat.mat_dvut_load(x))
        self.ui.opt_but_truba_kv.clicked.connect(lambda _, x=self: osn_mat.mat_truba_kv_load(x))
        self.ui.opt_but_kv.clicked.connect(lambda _, x=self: osn_mat.mat_kv_load(x))
        self.ui.opt_but_shestig.clicked.connect(lambda _, x=self: osn_mat.mat_shestigr_load(x))


        action_docs = self.ui.action_Docs
        action_docs.triggered.connect(self.zapusk_docs)

        action_dse = self.ui.action_reload_dse
        action_dse.triggered.connect(self.obnov_dse)

        action_obn_mat_erp = self.ui.action_sinc_mat
        action_obn_mat_erp.triggered.connect(self.obn_mat_erp)

        CMS.add_menu(self)
        # spis = CSQ.spis_iz_bd_sql(F.bdcfg('Naryad'), 'dse',shapka=False)
        # for i in range(len(spis)):
        #    old = spis[i][2]
        #    new = F.ochist_strok_pod_ima_fila(old)
        #    CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse',{'Наименование':new},{'Пномер':spis[i][0]})

        self.app_icons()
        self.obnov_dse()

    def app_icons(self):
        # from PyQt5.QtGui import QIcon
        # from PyQt5.QtWidgets import QApplication, QStyle
        self.ui.pushButton_sozd.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_ComputerIcon)))
        self.ui.pushButton_sozd.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_vigruzit.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DriveFDIcon)))
        self.ui.pushButton_vigruzit.setIconSize(QtCore.QSize(32, 32))
        self.ui.btn_process.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogDetailedView)))
        self.ui.btn_process.setIconSize(QtCore.QSize(16, 16))
        self.ui.btn_normi.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_TitleBarMaxButton)))
        self.ui.btn_normi.setIconSize(QtCore.QSize(16, 16))
        self.ui.btn_mater.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogListView)))
        self.ui.btn_mater.setIconSize(QtCore.QSize(16, 16))
        self.ui.btn__open_docs.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DesktopIcon)))
        self.ui.btn__open_docs.setIconSize(QtCore.QSize(16, 16))
        self.ui.pushButton_Vverh.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowUp)))
        self.ui.pushButton_Vverh.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_Vniz.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowDown)))
        self.ui.pushButton_Vniz.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_Copy.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogNewFolder)))
        self.ui.pushButton_Copy.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_Paste.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogEnd)))
        self.ui.pushButton_Paste.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_Del.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton)))
        self.ui.pushButton_Del.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_otm_i_vihod.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxCritical)))
        self.ui.pushButton_otm_i_vihod.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_dob_doc.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileLinkIcon)))
        self.ui.pushButton_dob_doc.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_prosm_doc.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogContentsView)))
        self.ui.pushButton_prosm_doc.setIconSize(QtCore.QSize(32, 32))
        self.ui.pushButton_del_doc.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton)))
        self.ui.pushButton_del_doc.setIconSize(QtCore.QSize(32, 32))
        self.ui.Button_t_kar.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)))
        self.ui.Button_t_kar.setIconSize(QtCore.QSize(32, 32))
        self.ui.Button_t_op.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)))
        self.ui.Button_t_op.setIconSize(QtCore.QSize(32, 32))
        self.ui.Button_t_per.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)))
        self.ui.Button_t_per.setIconSize(QtCore.QSize(32, 32))
        self.ui.Button_create_mater.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogNewFolder)))
        self.ui.Button_create_mater.setIconSize(QtCore.QSize(32, 32))
        self.ui.Button_del_mater.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton)))
        self.ui.Button_del_mater.setIconSize(QtCore.QSize(32, 32))
        self.ui.Button_prim_mat.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)))
        self.ui.Button_prim_mat.setIconSize(QtCore.QSize(32, 32))
        self.ui.btn_prim_shablon_op.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)))
        self.ui.btn_prim_shablon_op.setIconSize(QtCore.QSize(32, 32))
        self.ui.btn_mag_prim.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MediaSeekBackward)))
        self.ui.btn_mag_prim.setIconSize(QtCore.QSize(32, 32))
        self.ui.btn_mag_napolky.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MediaSkipForward)))
        self.ui.btn_mag_napolky.setIconSize(QtCore.QSize(32, 32))
        self.ui.btn_mag_up.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowUp)))
        self.ui.btn_mag_up.setIconSize(QtCore.QSize(32, 32))
        self.ui.btn_mag_down.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowDown)))
        self.ui.btn_mag_down.setIconSize(QtCore.QSize(32, 32))
        self.ui.btn_mag_sbros.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_BrowserStop)))
        self.ui.btn_mag_sbros.setIconSize(QtCore.QSize(32, 32))

    def keyReleaseEvent(self, e):
        item = self.ui.tree.currentItem()
        # t#odo РАЗРЕШИТЬ ПЕРЕХОДЫ?
        # t#odo РАЗРЕШИТЬ ОБОРУДОВАНИЕ, ДОКУМЕНТЫ, ОСНАСТКУ ИНСТРУМЕНТ
        if self.ui.tbl_magaz_filtr.hasFocus():
            CMS.primenit_filtr(self, self.ui.tbl_magaz_filtr, self.ui.tbl_magaz)
        if self.ui.tblw_dse_find.hasFocus():
            CMS.primenit_filtr(self, self.ui.tblw_dse_find, self.ui.tblw_dse)
        if self.ui.tblw_dse.hasFocus():
            if e.key() == 16777220:
                nk_teg = CQT.nom_kol_po_imen(self.ui.tblw_dse, 'Теги')
                if self.ui.tblw_dse.currentColumn() == nk_teg:
                    nk_tk = CQT.nom_kol_po_imen(self.ui.tblw_dse, 'Номер_техкарты')
                    nom_row = self.ui.tblw_dse.currentRow()
                    CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Теги': self.ui.tblw_dse.item(nom_row, nk_teg).text()},
                                      {
                                          'Номер_техкарты': self.ui.tblw_dse.item(nom_row, nk_tk).text()
                                      })
        if self.ui.tbl_magaz.hasFocus():
            if e.key() == 16777220:
                nk_teg = CQT.nom_kol_po_imen(self.ui.tbl_magaz, 'Теги')
                if self.ui.tbl_magaz.currentColumn() == nk_teg:
                    nk_block = CQT.nom_kol_po_imen(self.ui.tbl_magaz, 'Пномер')
                    nom_row = self.ui.tbl_magaz.currentRow()
                    CSQ.update_bd_sql(CMS.tmp_dir() + F.sep() + 'mag.db', 'blocks',
                                      {'Теги': self.ui.tbl_magaz.item(nom_row, nk_teg).text()}, {
                                          'Пномер': self.ui.tbl_magaz.item(nom_row, nk_block).text()
                                      })
        if self.ui.tap_per.hasFocus():
            if e.key() == 16777220:
                if self.ui.tap_per.currentColumn() == 2:
                    self.obnovt_drevo_s_tab2_per()

        if self.ui.tap_per_osnast.hasFocus():
            if e.key() == 16777220:
                cu = self.ui.tap_per_osnast
                if cu.rowCount() == 0:
                    return
                print("Нажата клавиша <Enter>")
                self.w2 = mywindow2(cu, "Оснастка", cu.currentRow())
                self.w2.showNormal()
                if cu.item(cu.currentRow(), 0) != None:
                    self.w2.ui2.lineEdit.setText(cu.item(cu.currentRow(), 0).text())
                self.w2.ui2.lineEdit.setFocus()
        if self.ui.tap_per_insrt.hasFocus():
            if e.key() == 16777220:
                cu = self.ui.tap_per_insrt
                if cu.rowCount() == 0:
                    return
                print("Нажата клавиша <Enter>")
                self.w2 = mywindow2(cu, "Инструмент", cu.currentRow())
                self.w2.showNormal()
                if cu.item(cu.currentRow(), 0) != None:
                    self.w2.ui2.lineEdit.setText(cu.item(cu.currentRow(), 0).text())
                self.w2.ui2.lineEdit.setFocus()
        if self.ui.tbl_oper_mat.hasFocus():
            if e.key() == QtCore.Qt.Key_F5:
                print("Нажата клавиша <F5>")
                self.add_line_mat()
            if e.key() == QtCore.Qt.Key_Return:
                self.ui.tableW_oper_mat.setFocus()
                return
            if e.key() == QtCore.Qt.Key_Up or e.key() == QtCore.Qt.Key_Down:
                self.obnovit_mater_tabl()
        if self.ui.tableW_oper_mat.hasFocus():
            tab = self.ui.tableW_oper_mat
            if e.key() == 16777216:  # esc
                self.ui.tbl_oper_mat.setFocus()
            if e.key() == QtCore.Qt.Key_F5:
                print("Нажата клавиша <F5>")
                self.add_line_mat()
            if e.key() == QtCore.Qt.Key_Delete:
                print("Нажата клавиша <Del>")
                self.del_mat()
            if e.key() == 16777220:
                print("Нажата клавиша <Enter>")
                if tab.rowCount() == 0:
                    return
                self.w2 = mywindow2(self.ui.tree, "Материал")
                self.w2.showNormal()
                self.w2.ui2.lineEdit.setFocus()
            if e.key() == QtCore.Qt.Key_S or e.key() == 1067:
                if e.modifiers() == QtCore.Qt.AltModifier:
                    print("Нажата клавиша <alt + Enter>")
                    self.zap_mat_v_tree()
        if self.ui.tab_op.hasFocus():
            if e.key() == 16777220:
                if self.ui.tab_op.currentRow() == None:
                    return
                if self.ui.tab_op.currentColumn() == 3:
                    self.w2 = mywindow2(self.ui.tree, "Раб_ц")
                    self.w2.showNormal()
                    self.w2.ui2.lineEdit.setFocus()
                if self.ui.tab_op.currentColumn() == 4:
                    self.w2 = mywindow2(self.ui.tree, "Оборудование")
                    self.w2.showNormal()
                    self.w2.ui2.lineEdit.setFocus()
                if self.ui.tab_op.currentColumn() == 7:
                    self.w2 = mywindow2(self.ui.tree, "Профессия")
                    self.w2.showNormal()
                    self.w2.ui2.lineEdit.setFocus()
            if e.modifiers() == QtCore.Qt.AltModifier:
                if e.key() == QtCore.Qt.Key_S or e.key() == 1067:
                    self.obnovt_drevo_s_tabl1_op()
                if e.key() == QtCore.Qt.Key_Down or e.key() == 16777237:
                    self.ui.tab_op_doc.setFocus()
        if self.ui.tab_op_doc.hasFocus():
            if e.key() == 16777220:
                if self.ui.tab_op_doc.currentRow() == None:
                    return
                if self.ui.tab_op_doc.rowCount() > 0:
                    if self.ui.tab_op_doc.currentRow() > 0:
                        if self.ui.tab_op_doc.item(self.ui.tab_op_doc.currentRow() - 1, 0) == None \
                                or self.ui.tab_op_doc.item(self.ui.tab_op_doc.currentRow() - 1, 0).text() == '':
                            CQT.msgbox("Не заполенена предыдушая запись")
                            return
                self.w2 = mywindow2(self.ui.tree, "Док_оп")
                self.w2.showNormal()
                self.w2.ui2.lineEdit.setFocus()
            if e.modifiers() == QtCore.Qt.AltModifier:
                if e.key() == QtCore.Qt.Key_Up or e.key() == 16777235:
                    self.ui.tab_op.setFocus()
                if e.key() == QtCore.Qt.Key_S or e.key() == 1067:
                    self.obnovt_drevo_s_tabl1_op()
        if self.ui.tab_tk_doc.hasFocus():
            if e.key() == 16777220:
                if self.ui.tab_tk_doc.currentRow() == None:
                    return
                self.w2 = mywindow2(self.ui.tree, "Док_тк")
                self.w2.showNormal()
                self.w2.ui2.lineEdit.setFocus()
                return
            if e.modifiers() == QtCore.Qt.AltModifier:
                if e.key() == QtCore.Qt.Key_Up or e.key() == 16777235:
                    self.ui.tab_kar.setFocus()

        # =====клавиши из древа
        if self.ui.tree.hasFocus():
            # =====================================ограничение по режиму
            if self.ogr_rezim() == False:
                if e.key() == QtCore.Qt.Key_Delete:
                    self.tree_del()
                if int(e.modifiers()) == 67108864:
                    if e.key() == QtCore.Qt.Key_C or e.key() == 67:
                        self.tree_copy_buf_n(self.ui.t_buff_0)
                    if e.key() == QtCore.Qt.Key_V or e.key() == 86:
                        self.tree_paste_buf_n(self.ui.t_buff_0)
                if int(e.modifiers()) == 100663296:
                    if e.key() == 33:
                        self.tree_copy_buf_n(self.ui.t_buff_1)
                        self.sohran_buff(1, self.ui.t_buff_1)
                    if e.key() == 50:
                        self.tree_copy_buf_n(self.ui.t_buff_2)
                        self.sohran_buff(2, self.ui.t_buff_2)
                    if e.key() == 35 or e.key() == 8470:
                        self.tree_copy_buf_n(self.ui.t_buff_3)
                        self.sohran_buff(3, self.ui.t_buff_3)
                    if e.key() == 36 or e.key() == 59:
                        self.tree_copy_buf_n(self.ui.t_buff_4)
                        self.sohran_buff(4, self.ui.t_buff_4)
                    if e.key() == 37:
                        self.tree_copy_buf_n(self.ui.t_buff_5)
                        self.sohran_buff(5, self.ui.t_buff_5)
                    if e.key() == 94:
                        self.tree_copy_buf_n(self.ui.t_buff_6)
                        self.sohran_buff(6, self.ui.t_buff_6)
                    if e.key() == 38 or e.key() == 63:
                        self.tree_copy_buf_n(self.ui.t_buff_7)
                        self.sohran_buff(7, self.ui.t_buff_7)
                    if e.key() == 42:
                        self.tree_copy_buf_n(self.ui.t_buff_8)
                        self.sohran_buff(8, self.ui.t_buff_8)
                    if e.key() == 40:
                        self.tree_copy_buf_n(self.ui.t_buff_9)
                        self.sohran_buff(9, self.ui.t_buff_9)
                if int(e.modifiers()) == 67108864:
                    if e.key() == 49:
                        self.tree_paste_buf_n(self.ui.t_buff_1)
                    if e.key() == 50:
                        self.tree_paste_buf_n(self.ui.t_buff_2)
                    if e.key() == 51:
                        self.tree_paste_buf_n(self.ui.t_buff_3)
                    if e.key() == 52:
                        self.tree_paste_buf_n(self.ui.t_buff_4)
                    if e.key() == 53:
                        self.tree_paste_buf_n(self.ui.t_buff_5)
                    if e.key() == 54:
                        self.tree_paste_buf_n(self.ui.t_buff_6)
                    if e.key() == 55:
                        self.tree_paste_buf_n(self.ui.t_buff_7)
                    if e.key() == 56:
                        self.tree_paste_buf_n(self.ui.t_buff_8)
                    if e.key() == 57:
                        self.tree_paste_buf_n(self.ui.t_buff_9)
                if e.key() == QtCore.Qt.Key_F5:
                    print("Нажата клавиша <F5>")
                    self.dobav_V_tree_root(self.ui.tree.topLevelItemCount() + 1)
                    # self.obnovit_param_tabl_kar()
                if e.key() == QtCore.Qt.Key_F6:
                    print("Нажата клавиша <F6>")

                    if item == None:
                        return
                    if item.text(item.columnCount() - 1) == "0":
                        uroven = item.text(3)
                        self.dobav_V_tree_oper(item, uroven)
                    if item.text(item.columnCount() - 1) == "1":
                        uroven = item.parent().text(3)
                        self.dobav_V_tree_oper(item.parent(), uroven)
                    self.obnovit_param_tabl_oper()
            # =====================================ограничение по режиму

            if e.key() == QtCore.Qt.Key_F7:
                print("Нажата клавиша <F7>")
                item = self.ui.tree.currentItem()
                if item == None:
                    return
                if item.text(item.columnCount() - 1) == "1":
                    uroven = item.text(3)
                    self.dobav_V_tree_perex(item, uroven)
                if item.text(item.columnCount() - 1) == "2":
                    uroven = item.parent().text(3)
                    self.dobav_V_tree_perex(item.parent(), uroven)
            if e.modifiers() == QtCore.Qt.ControlModifier and e.key() == 16777220:  # ввод через интер операции перехода карты
                self.w2 = mywindow2(self.ui.tree, "Древо")
                self.w2.showNormal()
                if self.ui.tree.currentItem() == None:
                    return
                self.w2.ui2.lineEdit.setText(self.ui.tree.currentItem().text(0))
                self.w2.ui2.textEdit.setText(self.ui.tree.currentItem().text(0))
                for i in range(self.w2.ui2.combo2.count()):
                    if self.ui.tree.currentItem().text(0) == self.w2.ui2.combo2.itemText(i):
                        self.w2.ui2.combo2.setCurrentIndex(i)
                        self.w2.vibor_elem2()
                        break
                self.w2.ui2.textEdit.setEnabled(False)
                self.w2.ui2.lineEdit.setFocus()

            if e.modifiers() == QtCore.Qt.AltModifier:  # ввод доп данных
                item = self.ui.tree.currentItem()
                if item == None:
                    return
                if item.text(item.columnCount() - 1) == "0":
                    if e.key() == QtCore.Qt.Key_D or e.key() == 1042:
                        cu = self.ui.tab_tk_doc
                        for i in range(cu.rowCount() - 1):
                            if cu.item(i, 0) == None or cu.item(i, 0).text() == "":
                                cu.selectRow(i)
                                break
                        self.w2 = mywindow2(cu, "Док_тк", cu.currentRow())
                        self.w2.showNormal()
                        if cu.item(cu.currentRow(), 0) != None:
                            self.w2.ui2.lineEdit.setText(cu.item(cu.currentRow(), 0).text())
                    if e.key() == QtCore.Qt.Key_S or e.key() == 1067:
                        self.obnovt_drevo_s_tabl3_kar()
                        return
                if item.text(item.columnCount() - 1) == "1":
                    if e.key() == QtCore.Qt.Key_D or e.key() == 1042:
                        cu = self.ui.tab_op_doc
                        for i in range(cu.rowCount() - 1):
                            if cu.item(i, 0) == None or cu.item(i, 0).text() == "":
                                cu.selectRow(i)
                                break
                        self.w2 = mywindow2(cu, "Док_оп", cu.currentRow())
                        self.w2.showNormal()
                        if cu.item(cu.currentRow(), 0) != None:
                            self.w2.ui2.lineEdit.setText(cu.item(cu.currentRow(), 0).text())
                    if e.key() == QtCore.Qt.Key_S or e.key() == 1067:
                        self.obnovt_drevo_s_tabl1_op()
                        return
                if item.text(item.columnCount() - 1) == "2":
                    if e.key() == QtCore.Qt.Key_Q or e.key() == 1049:
                        cu = self.ui.tap_per_osnast
                        for i in range(cu.rowCount() - 1):
                            if cu.item(i, 0) == None or cu.item(i, 0).text() == "":
                                cu.selectRow(i)
                                break
                        self.w2 = mywindow2(cu, "Оснастка", cu.currentRow())
                        self.w2.showNormal()
                        if cu.item(cu.currentRow(), 0) != None:
                            self.w2.ui2.lineEdit.setText(cu.item(cu.currentRow(), 0).text())
                        # self.w2.ui2.lineEdit.setFocus()
                    if e.key() == QtCore.Qt.Key_W or e.key() == 1062:
                        cu = self.ui.tap_per_insrt
                        for i in range(cu.rowCount() - 1):
                            if cu.item(i, 0) == None or cu.item(i, 0).text() == "":
                                cu.selectRow(i)
                                break
                        self.w2 = mywindow2(cu, "Инструмент", cu.currentRow())
                        self.w2.showNormal()
                        if cu.item(cu.currentRow(), 0) != None:
                            self.w2.ui2.lineEdit.setText(cu.item(cu.currentRow(), 0).text())
                        # self.w2.ui2.lineEdit.setFocus()
                    if e.key() == QtCore.Qt.Key_S or e.key() == 1067:
                        self.obnovt_drevo_s_tab2_per()
                        return
            return

        # ==движение по вкладкам и таблицам
        if e.modifiers() == QtCore.Qt.AltModifier:
            if e.key() == QtCore.Qt.Key_Z or e.key() == 1071:
                self.ui.tree.setFocus()
                self.ui.tabW.setCurrentIndex(0)
            if e.key() == QtCore.Qt.Key_X or e.key() == 1063:
                if item.text(item.columnCount() - 1) == "0":
                    self.ui.tab_kar.setFocus()
                if item.text(item.columnCount() - 1) == "1":
                    self.ui.tab_op.setFocus()
                if item.text(item.columnCount() - 1) == "2":
                    self.ui.tap_per.setFocus()
                self.ui.tabW.setCurrentIndex(0)
            if e.key() == QtCore.Qt.Key_C or e.key() == 1057:
                self.ui.tbl_oper_mat.setFocus()
                self.ui.tabW.setCurrentIndex(1)
            if e.key() == QtCore.Qt.Key_V or e.key() == 1052:
                self.ui.tabW.setCurrentIndex(2)
            if self.ui.tap_per.hasFocus():
                if e.key() == QtCore.Qt.Key_Down or e.key() == 16777237:
                    self.ui.tap_per_osnast.setFocus()
                    return
            if self.ui.tap_per_osnast.hasFocus():
                if e.key() == QtCore.Qt.Key_Down or e.key() == 16777237:
                    self.ui.tap_per_insrt.setFocus()
                    return
                if e.key() == QtCore.Qt.Key_Up or e.key() == 16777235:
                    self.ui.tap_per.setFocus()
                    return
            if self.ui.tap_per_insrt.hasFocus():
                if e.key() == QtCore.Qt.Key_Up or e.key() == 16777235:
                    self.ui.tap_per_osnast.setFocus()
                    return
            if self.ui.tab_kar.hasFocus():
                if e.key() == QtCore.Qt.Key_Down or e.key() == 16777237:
                    self.ui.tab_tk_doc.setFocus()
                    return
        return


    def load_param_from_dxf(self,sp_tree):
        # ==================DXF==========================
        self.global_param_tk_dxf = ''
        flag = False
        for i in range(len(sp_tree)):
            if len(sp_tree[i]) >= 20:
                if sp_tree[i][20] == '0' and flag:
                    return
                if sp_tree[i][20] == '0' and flag == False:
                    flag = True
                if sp_tree[i][20] == '1'and sp_tree[i][0] == 'Резка(ЧПУ)' and sp_tree[i][4] == '010101':
                    if sp_tree[i][15] != '':
                        file_prikr = sp_tree[i][15]
                        if F.ostavit_rasshir(file_prikr) == '.dxf':
                            dict_rez = CDXF.raschet_dxf(db_files_load(file_prikr))
                            if dict_rez != None:
                                self.global_param_tk_dxf = dict_rez
                            else:
                                CQT.msgbox('DXF не корректный, не распознать.')
        # ===============================================

    def obn_mat_erp(self):
        if CQT.msgboxgYN('Произойдет загрузка материалов из ЕРП и синхронизация баз, это займет около 5 минут. Продолжаем?'):
            rez = nomen_erp.general()
            if rez == True:
                CQT.msgbox('Базы успешно обновлены')
            else:
                CQT.msgbox(rez)


    def zagruz_mat_iz_nomenklatyri(self):
        tbl = self.ui.tableW_oper_mat
        if tbl.currentRow() == -1:
            CQT.msgbox('Не выбрана строка материала')
            return
        nk_kod = CQT.nom_kol_po_imen(tbl,'Код')
        nk_mat = CQT.nom_kol_po_imen(tbl,'Материал')
        nk_edizm = CQT.nom_kol_po_imen(tbl,'Ед.Изм')
        nk_norm = CQT.nom_kol_po_imen(tbl,'Норма')
        zapros = f"""SELECT Код_ЕРП FROM dse WHERE Номенклатурный_номер == '{self.dse_nn}' AND Наименование == '{self.dse_naim}' """
        rez = CSQ.zapros(F.bdcfg('Naryad'),zapros)
        if rez[1][0] == '':
            CQT.msgbox('Код не определен в БД')
            return
        else:
            kod = rez[1][0].strip()
            if F.nalich_file(F.scfg('cash') + os.sep + "bd_mater.txt"):
                spisok = F.otkr_f(F.scfg('cash') + os.sep + "bd_mater.txt", False, separ='|')
                nk_mat_nn = F.nom_kol_po_im_v_shap(spisok, 'НН')
                nk_mat_naim = F.nom_kol_po_im_v_shap(spisok, 'Наименование')
                nk_mat_ed = F.nom_kol_po_im_v_shap(spisok, 'Ед.измерения')
                flag_naid = False
                for i in range(1, len(spisok)):
                    if spisok[i][nk_mat_nn].strip() == kod:
                        tbl.item(tbl.currentRow(),nk_kod).setText(kod)
                        tbl.item(tbl.currentRow(), nk_mat).setText(spisok[i][nk_mat_naim])
                        tbl.item(tbl.currentRow(), nk_edizm).setText(spisok[i][nk_mat_ed])
                        tbl.item(tbl.currentRow(), nk_norm).setText('*')
                        flag_naid = True
                        break
                if flag_naid == False:
                    CQT.msgbox(f'Не найден {kod} в bd_mater')


    def obnov_dse(self):
        tabl_bd = self.ui.tblw_dse
        row = False
        if tabl_bd.currentRow() != None and tabl_bd.currentRow() != -1:
            row = tabl_bd.currentRow()
        spis_filtr = CQT.spisok_iz_wtabl(self.ui.tblw_dse_find)
        stroki = CSQ.spis_iz_bd_sql(F.bdcfg('Naryad'), 'dse', True, True)
        self.set_kol_bd_dse = {0, 1, 2, 3, 6, 7, 8, 9, 10,11,12,13}

        CQT.zapoln_wtabl(self, stroki, tabl_bd, self.set_kol_bd_dse, {F.nom_kol_po_im_v_shap(stroki, 'Тех_заметки') - 2,
                                                                      F.nom_kol_po_im_v_shap(stroki, 'Теги') - 2},
                         isp_shapka=True, separ='', max_vis_row=20)
        # CQT.zapoln_vtabl(self,tabl_bd,stroki,isp_shapka = True, separ= '')
        tabl_bd.horizontalHeader().setStretchLastSection(True)
        CMS.zapolnit_filtr(self, self.ui.tblw_dse_find, tabl_bd)
        if row:
            tabl_bd.setCurrentCell(row,0)
        CMS.zapolnit_filtr(self, self.ui.tblw_dse_find, tabl_bd, spis_filtr)



    def tex_zametki(self):
        tbl = self.ui.tblw_dse
        row = tbl.currentRow()
        if row == -1:
            return
        n_k_nn = CQT.nom_kol_po_imen(tbl, 'Номенклатурный_номер')
        n_k_naim = CQT.nom_kol_po_imen(tbl, 'Наименование')
        n_k_texzam = CQT.nom_kol_po_imen(tbl, 'Тех_заметки')
        CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Тех_заметки': tbl.item(row, n_k_texzam).text()}, {
            'Номенклатурный_номер': tbl.item(row, n_k_nn).text(),
            'Наименование': tbl.item(row, n_k_naim).text()
        })

    def export_csv_op(self, spis_tk, nn, naim):
        if 'ПУ0' in naim:
            ima = nn + "$" + naim
        else:
            ima = nn + "$" + F.ochist_strok_pod_ima_fila(naim)
        n_k_ur = 20
        n_k_op = 0
        n_k_tpz = 6
        n_k_tsh = 7
        flag_tk = False
        rez_sp = [["Операция", 'Тпз', 'Тшт']]
        for i in range(len(spis_tk)):
            if spis_tk[i][n_k_ur] == '0':
                if flag_tk:
                    break
                else:
                    flag_tk = True
            if spis_tk[i][n_k_ur] == '1':
                rez_sp.append([spis_tk[i][n_k_op], spis_tk[i][n_k_tpz], spis_tk[i][n_k_tsh]])
        if F.nalich_file(F.scfg('defolt_fold') + os.sep + "csv") == False:
            F.sozd_dir(F.scfg('defolt_fold') + os.sep + "csv")
        F.zap_f(F.scfg('defolt_fold') + os.sep + "csv" + os.sep + ima + '.csv', rez_sp, separ='|', utf8=True)

    def zagruzit_old_tk(self, row, col):
        kol_nom_mk = CQT.nom_kol_po_imen(self.ui.tbl_isp_mk, 'Пномер')
        if kol_nom_mk == None:
            return
        nom_mk = self.ui.tbl_isp_mk.item(row, kol_nom_mk).text()
        self.vibor_dse(nom_mk)
        self.load_redaktor_tk(nom_mk)
        self.sozd_file(nom_mk)
        self.ui.pushButton_Vverh.setEnabled(False)
        self.ui.pushButton_Vniz.setEnabled(False)
        self.ui.pushButton_Copy.setEnabled(False)
        self.ui.pushButton_Paste.setEnabled(False)
        self.ui.pushButton_Del.setEnabled(False)
        # t#odo ОТКЛЮЧИТЬ КОНОПКИ ВВЕРХ,ВНИЗ, ВСТАВИТЬ, УДАЛИТЬ,КОПИРОВАТЬ
        # t#odo ЗАБЛОКИРОВАТЬ РЕДАКТИРОВАНИЕ РАБОЧИХ ЦЕНТРОВ, НАЗВАНИЯ ОПЕРАЦИЙ, НОМЕРВ

    def ogr_rezim(self):
        if 'по маршрутной карте' in self.windowTitle():
            return True
        return False

    def nalichie_nevip_mk(self):
        tbl_dse = self.ui.tblw_dse
        nk_nn = CQT.nom_kol_po_imen(tbl_dse,'Номенклатурный_номер')
        nk_naim = CQT.nom_kol_po_imen(tbl_dse, 'Наименование')
        nn = tbl_dse.item(tbl_dse.currentRow(),nk_nn).text()
        naim = tbl_dse.item(tbl_dse.currentRow(), nk_naim).text()
        #nn  = self.windowTitle().split('_')[1]
        # ntk = self.windowTitle().split('_')[0]
        #naim = self.windowTitle().split('_')[2]
        flag_naid = False
        if F.nalich_file(F.bdcfg('Naryad')) == False:
            CQT.zapoln_wtabl(self, [['Не найдена БД Naryad']], self.ui.tbl_isp_mk, isp_shapka=False, separ='')
            return flag_naid
        try:
            zapros = f'''SELECT Пномер,Дата,Статус, Номер_заказа, Номер_проекта,Вид,Ресурсная FROM mk WHERE
                        Прогресс != "Завершено" AND Статус == "Открыта" '''
            spis_mk = CSQ.zapros(F.bdcfg('Naryad'),zapros)
            #spis_mk = CSQ.naiti_v_bd(F.bdcfg('Naryad'), 'mk', {'Прогресс': 'Завершено'}, shapka=True, ne=True)
            spis_mk_rez = [["Пномер","Дата","Статус", "Номер_заказа", "Номер_проекта","Вид"]]
            nk_res = F.nom_kol_po_im_v_shap(spis_mk,'Ресурсная')
            for i in range(1, len(spis_mk)):
                #sp_mk_det = F.otkr_f(F.scfg('Naryad') + os.sep + str(spis_mk[i][nom_kol_mk]) + '.txt', False, '|')
                if spis_mk[i][nk_res] != "":
                    sp_mk_det = F.from_binary_pickle(spis_mk[i][nk_res])
                    if sp_mk_det == ['']:
                        continue
                    for j in range(len(sp_mk_det)):
                        if sp_mk_det[j]['Наименование'].strip() == naim and sp_mk_det[j]['Номенклатурный_номер'].strip() == nn:
                            flag_naid = True
                            spis_mk_rez.append([spis_mk[i][0],spis_mk[i][1],spis_mk[i][2],spis_mk[i][3],spis_mk[i][4],spis_mk[i][5]])
                            break
            set_isp_kol = {0, 1, 2, 3, 4, 5}
            CQT.zapoln_wtabl(self, spis_mk_rez, self.ui.tbl_isp_mk, isp_shapka=True, separ='',
                             set_isp_nomera_col=set_isp_kol)
            return flag_naid
        except:
            CQT.zapoln_wtabl(self, [['Ошибка']], self.ui.tbl_isp_mk, isp_shapka=False, separ='')
            return flag_naid

    def zapusk_docs(self):
        tbl = self.ui.tblw_dse
        strok = tbl.currentRow()
        kol_naim = CQT.nom_kol_po_imen(tbl, 'Наименование')
        kol_nn = CQT.nom_kol_po_imen(tbl, 'Номенклатурный_номер')
        if strok == -1:
            if self.dse_nn == '':
                CQT.msgbox('Не выбрана ТК')
                return
            nn_det = self.dse_nn
            naim =self.dse_naim
        else:
            nn_det = tbl.item(strok, kol_nn).text()
            naim = tbl.item(strok, kol_naim).text()
        CMS.zapustit_ssicy_docs(nn_det, naim)
        # F.zapyst_file(adres,False)

    def del_mat(self):
        tab = self.ui.tableW_oper_mat
        tab.removeRow(tab.currentRow())

    def status_process(self):
        rez = CQT.msgboxgYN('Изменить статус готовности процесса?')
        if rez == False:
            return
        tbl = self.ui.tblw_dse
        row = tbl.currentRow()
        n_k_process = CQT.nom_kol_po_imen(tbl, 'Процесс')
        n_k_nn = CQT.nom_kol_po_imen(tbl, 'Номенклатурный_номер')
        n_k_naim = CQT.nom_kol_po_imen(tbl, 'Наименование')
        if tbl.item(row, n_k_process).text() == '1':
            tbl.item(row, n_k_process).setText('0')
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Процесс': 0}, {
                'Номенклатурный_номер': tbl.item(row, n_k_nn).text(),
                'Наименование': tbl.item(row, n_k_naim).text()
            })
        else:
            tbl.item(row, n_k_process).setText('1')
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Процесс': 1}, {
                'Номенклатурный_номер': tbl.item(row, n_k_nn).text(),
                'Наименование': tbl.item(row, n_k_naim).text()
            })

    def status_mater(self):
        rez = CQT.msgboxgYN('Изменить статус готовности норм материалов?')
        if rez == False:
            return
        tbl = self.ui.tblw_dse
        row = tbl.currentRow()
        n_k_process = CQT.nom_kol_po_imen(tbl, 'Материалы')
        n_k_nn = CQT.nom_kol_po_imen(tbl, 'Номенклатурный_номер')
        n_k_naim = CQT.nom_kol_po_imen(tbl, 'Наименование')
        if tbl.item(row, n_k_process).text() == '1':
            tbl.item(row, n_k_process).setText('0')
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Материалы': 0}, {
                'Номенклатурный_номер': tbl.item(row, n_k_nn).text(),
                'Наименование': tbl.item(row, n_k_naim).text()
            })
        else:
            tbl.item(row, n_k_process).setText('1')
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Материалы': 1}, {
                'Номенклатурный_номер': tbl.item(row, n_k_nn).text(),
                'Наименование': tbl.item(row, n_k_naim).text()
            })

    def status_normi(self):
        rez = CQT.msgboxgYN('Изменить статус готовности норм времени?')
        if rez == False:
            return
        tbl = self.ui.tblw_dse
        row = tbl.currentRow()
        n_k_process = CQT.nom_kol_po_imen(tbl, 'Нормы')
        n_k_nn = CQT.nom_kol_po_imen(tbl, 'Номенклатурный_номер')
        n_k_naim = CQT.nom_kol_po_imen(tbl, 'Наименование')
        if tbl.item(row, n_k_process).text() == '1':
            tbl.item(row, n_k_process).setText('0')
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Нормы': 0}, {
                'Номенклатурный_номер': tbl.item(row, n_k_nn).text(),
                'Наименование': tbl.item(row, n_k_naim).text()
            })
        else:
            tbl.item(row, n_k_process).setText('1')
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Нормы': 1}, {
                'Номенклатурный_номер': tbl.item(row, n_k_nn).text(),
                'Наименование': tbl.item(row, n_k_naim).text()
            })

    def add_line_mat(self):
        tab = self.ui.tableW_oper_mat
        if tab.rowCount() > 0:
            for i in range(0, tab.columnCount()):
                if tab.item(tab.rowCount() - 1, i) == None:
                    CQT.msgbox("Не заполенена предыдушая запись")
                    return
        tab.setRowCount(tab.rowCount() + 1)

    def prov_filtr(self, text, stroka, kolonka, spisok, spis_rez):
        if len(text) > 0:
            if text[0] == '!':
                if text[1:] == "*":
                    if str(spisok[stroka][kolonka]) != "":
                        return False
                else:
                    if text[1:] in str(spisok[stroka][kolonka]):
                        return False
            if text[0] == '=':
                for i in range(1, len(spis_rez)):
                    if spis_rez[i][kolonka] == str(spisok[stroka][kolonka]):
                        return False
            if text[0] != '!':
                if text[0] == "*":
                    if str(spisok[stroka][kolonka]) == '':
                        return False
                else:
                    if text.replace('=', '') not in str(spisok[stroka][kolonka]):
                        return False
        return True

    def otm_i_vihod(self):
        n_dse = self.ui.lineEdit_dse
        n_tk = self.ui.lineEdit_nntk
        naim_dse = self.ui.lineEdit_dse_naim
        ima = n_tk.text() + '_' + n_dse.text() + ".txt"
        tmpf = F.put_po_umolch() + os.sep + "tmp_tk"
        vosst_mk = False
        if 'по маршрутной карте' in self.windowTitle():
            vosst_mk = True
            nom_mk = self.windowTitle().split('карте ')[-1]
        self.ui.tabWidget.setTabEnabled(1, False)
        if vosst_mk:
            relf = F.scfg('Naryad') + os.sep + nom_mk + os.sep + ima.replace('.txt', '.pickle')
        else:
            relf = F.scfg("add_docs") + os.sep + ima.replace('.txt', '.pickle')
        if F.nalich_file(tmpf):
            rez = F.skopir_file(tmpf, relf)
            if rez == False:
                print(False)
            F.udal_file(tmpf)
        self.unblock_tk(naim_dse.text(), n_dse.text())

    def cvet_knopki(self):
        tabl = self.ui.tab_op
        tabl_1 = self.ui.tab_op_doc
        tab2 = self.ui.tap_per
        tab21 = self.ui.tap_per_insrt
        tab22 = self.ui.tap_per_osnast
        tab3 = self.ui.tab_kar
        tab31 = self.ui.tab_tk_doc
        butt_op = self.ui.Button_t_op
        butt_kar = self.ui.Button_t_kar
        butt_per = self.ui.Button_t_per
        tree = self.ui.tree
        if tabl.hasFocus() or tabl_1.hasFocus():
            CQT.ust_cvet_text_obj(butt_op, 225, 10, 10)
        if tab2.hasFocus() or tab21.hasFocus() or tab22.hasFocus():
            CQT.ust_cvet_text_obj(butt_per, 225, 10, 10)
        if tab3.hasFocus() or tab31.hasFocus():
            CQT.ust_cvet_text_obj(butt_kar, 225, 10, 10)
        if tree.hasFocus():
            CQT.ust_cvet_text_obj(butt_op, 180, 180, 170)
            CQT.ust_cvet_text_obj(butt_per, 180, 180, 170)
            CQT.ust_cvet_text_obj(butt_kar, 180, 180, 170)


    def vigruzit(self):
        sp = GF3(self)
        # for i in sp:
        #   print(i)
        # return
        if sp == None:
            return
        n_tk = self.ui.lineEdit_nntk
        putt = F.scfg('vivod_tk')
        if F.nalich_file(putt) == False:
            F.sozd_dir(putt)
        if len(putt) < 3:
            putt = os.path.expanduser('~')
        ima = CQT.f_dialog_save(self, "Сохранить", putt + os.sep + n_tk.text() + '.txt', 'Текст файл(*.txt);;Все(*.*)')
        if ima == ".":
            return
        F.zap_f(ima, sp)
        CQT.msgbox("Файл " + ima + " сохранен")
        F.zapyst_file(ima)

    def block_tk(self, naim, nn):
        dost = CSQ.naiti_v_bd(F.bdcfg('Naryad'), 'dse', {'Номенклатурный_номер': nn, 'Наименование': naim}, ['Доступ'],
                              all=False)
        if dost == None:
            return False
        dost = dost[0]
        if dost == "" or dost == None:
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse',
                              {'Доступ': F.user_name()},
                              {'Номенклатурный_номер': nn, 'Наименование': naim})
            return True
        if dost == F.user_name():
            return True
        return dost

    def unblock_tk(self, naim, nn):
        dost = CSQ.naiti_v_bd(F.bdcfg('Naryad'), 'dse', {'Номенклатурный_номер': nn, 'Наименование': naim}, ['Доступ'],
                              all=False)
        if dost == None:
            return False
        dost = dost[0]
        if F.user_name() == dost:
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse',
                              {'Доступ': ''},
                              {'Номенклатурный_номер': nn, 'Наименование': naim})
            return True
        if dost == '' or dost == None:
            return True
        return False

    def zagr_tk(self, po_mk=False):
        n_dse = self.ui.lineEdit_dse
        nazv_dse = self.ui.lineEdit_dse_naim
        n_tk = self.ui.lineEdit_nntk

        if nazv_dse.text() == '':
            CQT.msgbox('Не заполнено название ДСЕ')
            return
        if n_tk.text() == '':
            CQT.msgbox('Не заполнен номер технологической карты')
            return
        ima = n_tk.text() + '_' + n_dse.text() + ".txt"
        if F.nalich_file(F.scfg("add_docs")) == False:
            CQT.msgbox('Не найден каталог с ТК')
            return

        if po_mk == False:
            spisok_tk = F.otkr_f(F.scfg("add_docs") + os.sep + ima, False, '|', pickl=True, propuski=True)
            if spisok_tk == ['']:
                rez = CQT.msgboxgYN('Не найдена ТК, Создать техкарту заново?')
                if rez:
                    CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse', {'Номер_техкарты': ''},
                                      {'Наименование': nazv_dse.text(),
                                       "Номенклатурный_номер": n_dse.text()})
                    self.obnov_dse()
                    return
                else:
                    return
            F.skopir_file(F.scfg("add_docs") + os.sep + ima.replace('.txt', '.pickle'),
                          F.put_po_umolch() + os.sep + "tmp_tk")

            self.setWindowTitle(n_tk.text() + '$' + n_dse.text() + "$" + nazv_dse.text())

        else:
            spisok_tk = F.otkr_f(F.scfg("Naryad") + os.sep + po_mk + os.sep + ima, False, '|', pickl=True, propuski=True)
            if spisok_tk == ['']:
                CQT.msgbox('Не найдена ТК')
                return
            F.skopir_file(F.scfg("Naryad") + os.sep + po_mk + os.sep + ima.replace('.txt', '.pickle'),
                          F.put_po_umolch() + os.sep + "tmp_tk")
            self.setWindowTitle(
                n_tk.text() + '$' + n_dse.text() + "$" + nazv_dse.text() + "$по маршрутной карте " + po_mk)
        self.nom_tk = n_tk.text()
        self.dse_nn = n_dse.text()
        self.dse_naim = nazv_dse.text()

        sp_tree = []
        for i in range(10, len(spisok_tk)):
            sp_tree.append(spisok_tk[i])
        self.zapoln_tree_spiskom(sp_tree)
        #self.load_param_from_dxf(sp_tree)
        self.ui.tree.setCurrentIndex(self.ui.tree.model().index(0, 0))
        return

    def save_tk_vklad(self):
        if self.ui.tabWidget.currentIndex() == 1:
            return
        self.save_shir_kol_tree()
        n_dse = self.ui.lineEdit_dse
        n_tk = self.ui.lineEdit_nntk
        naim_dse = self.ui.lineEdit_dse_naim
        self.unblock_tk(naim_dse.text(), n_dse.text())
        self.save_tk()
        self.ui.tabWidget.setTabEnabled(1, False)
        self.setWindowTitle(F.put_po_umolch())
        self.nom_tk = ''
        self.dse_nn = ''
        self.dse_naim = ''
        self.ui.pushButton_sozd.setEnabled(True)

    def btn_prim_izm_shablon(self):
        if F.nalich_file(self.PUT_K_TMP) == False:
            F.sozd_dir(self.PUT_K_TMP)
        putf = self.PUT_K_TMP + os.sep + "shablon_op.txt"
        spis = CQT.spisok_iz_wtabl(self.ui.tbl_shablon_op, "", True)
        F.zap_f(putf, spis, separ='|')
        CQT.msgbox("Успешно")

    def tab_click(self, ind):
        print(int)
        self.widths()
        if ind == 1:
            self.obnovit_param_tabl_oper_mat()
        if ind == 2:
            pass
        if ind == 3:
            putf = self.PUT_K_TMP + os.sep + "shablon_op.txt"
            if F.nalich_file(F.scfg('cash') + os.sep + "oper.txt"):
                spis_op = F.otkr_f(F.scfg('cash') + os.sep + "oper.txt", False, "|")
            else:
                CQT.msgbox('Не найден список операций')
                return
            if F.nalich_file(putf):
                spis_sh = F.otkr_f(putf, False, "|")
            else:
                spis_sh = []
            rez = [['Операция', 'Рабочий ценр', 'Оборудование', 'Профессия', 'Документация($)']]
            for i in range(len(spis_op)):
                ima = spis_op[i][0]
                rc = ''
                obor = ''
                prof = ''
                doc = ''
                for j in range(1, len(spis_sh)):
                    if ima == spis_sh[j][0]:
                        rc = spis_sh[j][1]
                        obor = spis_sh[j][2]
                        prof = spis_sh[j][3]
                        doc = '' if len(spis_sh[j]) < 5 else spis_sh[j][4]
                        break
                rez.append([ima, rc, obor, prof, doc])
            set_red = {1, 2, 3, 4}
            CQT.zapoln_wtabl(self, rez, self.ui.tbl_shablon_op, separ='', isp_shapka=True,
                             set_editeble_col_nomera=set_red)
        if ind == 4:
            if F.nalich_file(CMS.tmp_dir() + F.sep() + 'mag.db') == False:
                frase_tmp = """CREATE TABLE IF NOT EXISTS blocks(
                   Пномер INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE ON CONFLICT ROLLBACK,
                   Статус INT,
                   Запись TEXT,
                   Теги TEXT
                   );
                """
                CSQ.sozd_bd_sql(CMS.tmp_dir() + F.sep() + 'mag.db', frase_tmp)
            self.load_magaz()
            CMS.zapolnit_filtr(self, self.ui.tbl_magaz_filtr, self.ui.tbl_magaz)

    def magazin_na_del(self):
        tbl = self.ui.tbl_magaz
        rez = CQT.msgboxgYN('Произойдет удаление выбранных галками блоков')
        if rez:
            list_check = []
            list_check_tbl = []
            nk_check = CQT.nom_kol_po_imen(tbl, 'Статус')
            nk_nom = CQT.nom_kol_po_imen(tbl, 'Пномер')
            for i in range(tbl.rowCount()):
                if tbl.cellWidget(i, nk_check).isChecked():
                    list_check.append(tbl.item(i, nk_nom).text())
                    list_check_tbl.append(i + 1)
            if list_check == []:
                CQT.msgbox('Не выбраны блоки')
                return
            rez = CQT.msgboxgYN(f'Подтверждаешь удаление блоков {list_check_tbl}?')
            if rez:
                conn, cur = CSQ.connect_bd(CMS.tmp_dir() + F.sep() + 'mag.db')
                for i in range(len(list_check)):
                    zapros = f'''
                        DELETE FROM blocks
                        WHERE Пномер='{list_check[i]}'; '''
                    CSQ.zapros('', zapros, conn)
                CSQ.close_bd(conn)
                self.load_magaz()

    def mag_down(self):
        tbl = self.ui.tbl_magaz
        cur_row = tbl.currentRow() + 1
        if cur_row > tbl.rowCount() - 1:
            return
        spis = CQT.spisok_iz_wtabl(tbl, shapka=True)
        spis[cur_row], spis[cur_row + 1] = spis[cur_row + 1], spis[cur_row]
        self.load_magaz(spis)
        tbl.setCurrentCell(cur_row, 2)

    def magazin_up(self):
        tbl = self.ui.tbl_magaz
        cur_row = tbl.currentRow() + 1
        if cur_row < 2:
            return
        spis = CQT.spisok_iz_wtabl(tbl, shapka=True)
        spis[cur_row], spis[cur_row - 1] = spis[cur_row - 1], spis[cur_row]
        self.load_magaz(spis)
        tbl.setCurrentCell(cur_row - 2, 2)

    def magazin_primenit(self):
        len_msg = 45
        tab = '    '
        tbl = self.ui.tbl_magaz
        list_check = []
        nk_check = CQT.nom_kol_po_imen(tbl, 'Статус')
        nk_nom = CQT.nom_kol_po_imen(tbl, 'Пномер')
        for i in range(tbl.rowCount()):
            if tbl.cellWidget(i, nk_check).isChecked():
                list_check.append(int(tbl.item(i, nk_nom).text()))
        if list_check == []:
            CQT.msgbox('Не выбраны блоки')
            return
        conn, cur = CSQ.connect_bd(CMS.tmp_dir() + F.sep() + 'mag.db')
        if len(list_check) == 1:
            zapros = f'''
                                            SELECT Пномер, Запись FROM blocks
                                            WHERE Пномер = {list_check[0]}; '''
        else:
            zapros = f'''
                                    SELECT Пномер, Запись FROM blocks
                                    WHERE Пномер IN {tuple(list_check)}; '''
        query = CSQ.zapros('', zapros, conn)
        CSQ.close_bd(conn)
        spis = []
        front_spis = []
        for k in range(len(list_check)):
            for i in range(1, len(query)):
                if query[i][0] == list_check[k]:
                    tmp = query[i][1].split('@')
                    for j in tmp:
                        spis.append(j.split('|'))
                        ur = int(spis[-1][20])
                        if len(j) > len_msg:
                            front_spis.append(tab * ur + j[:len_msg] + '...')
                        else:
                            front_spis.append(tab * ur + j)
                    break
        frase = "\n".join(front_spis)
        rez = CQT.msgboxgYN(f'Подтверждаешь применение к ТК, блоков?:\n{frase}')
        if rez == False:
            return

        tree = self.ui.tree
        item = tree.currentItem()
        spis_dreva = CQT.spisok_dreva(tree)
        if item == None:
            cur_str = ''
        else:
            cur_str = self.ui.tree.currentItem().text(3)
        cur_row = -1
        for i in range(len(spis_dreva)):
            if spis_dreva[i][3] == cur_str:
                cur_row = i
                break
        celev_row = len(spis_dreva) - 1
        cur_ur = int(spis[0][20])
        for i in range(cur_row + 1, len(spis_dreva)):
            if int(spis_dreva[i][20]) <= cur_ur:
                celev_row = i - 1
                break
        cur_row = celev_row
        for i in range(len(spis) - 1, -1, -1):
            spis_dreva.insert(cur_row + 1, spis[i])
        rez = []
        ur = -1
        for i in range(len(spis_dreva)):
            obr_ur = int(spis_dreva[i][20])
            if obr_ur == ur or obr_ur == ur + 1 or obr_ur < ur:
                rez.append(spis_dreva[i])
                ur = obr_ur
        self.zapoln_tree_spiskom(rez)
        CQT.videlit_tree_znach(self.ui.tree, 3, cur_str)

    def magazin_na_polky(self):
        tree = self.ui.tree
        item = tree.currentItem()
        if item == None:
            return
        obr = item.text(3)
        tmp = []
        spisok = CQT.spisok_dreva(tree)
        for i in range(0, len(spisok)):
            if obr in spisok[i][3]:
                stroka = [x.replace('|', '-') for x in spisok[i]]
                stroka = [x.replace('@', '-') for x in stroka]
                if stroka[20] == '1' or stroka[20] == '2':
                    #stroka[6] = '*'  # тпз
                    stroka[7] = '*'  # тшт
                if stroka[20] == '1':
                    stroka[10] = ''  # материал
                stroka[15] = ''  # имя файла прикрепления
                stroka[1] = ''  # отметка ... файла прикрепления

                tmp.append(stroka)

        for i in range(len(tmp)):  # удаление чило дхф
            if tmp[i][20] == '2' and (tmp[i - 1][4] == '010101' or tmp[i - 1][4] == '010100') and 'ЧПУ' in tmp[i - 1][
                0]:
                if 'част' in tmp[i][0].lower() or 'егмент' in tmp[i][0].lower() or 'сектор' in tmp[i][0].lower():
                    tmp[i][0] = 'Сегменты ?'
        for i in range(len(tmp)):
            tmp[i] = '|'.join(tmp[i])
        zapis = '@'.join(tmp)
        CSQ.dob_strok_v_bd_sql(CMS.tmp_dir() + F.sep() + 'mag.db', 'blocks', [[0, zapis, '']], s_pervoi=False)
        self.load_magaz()
        return

    def load_magaz(self, spis=False):
        tab = '    '
        tbl = self.ui.tbl_magaz
        # spis = CSQ.spis_iz_bd_sql(CMS.tmp_dir() + F.sep() + 'mag.db','blocks',shapka=True)
        if spis == False:
            zapros = f'''SELECT * FROM blocks'''
            spis = CSQ.zapros(CMS.tmp_dir() + F.sep() + 'mag.db', zapros=zapros)
        rez = [spis[0]]
        nk_zapis = F.nom_kol_po_im_v_shap(spis, 'Запись')
        nk_teg = F.nom_kol_po_im_v_shap(spis, 'Теги')
        nk_pnom = F.nom_kol_po_im_v_shap(spis, 'Пномер')
        nk_stat = F.nom_kol_po_im_v_shap(spis, 'Статус')
        for i in range(1, len(spis)):
            rez.append([spis[i][nk_pnom], str(spis[i][nk_stat]), spis[i][nk_zapis], spis[i][nk_teg]])

        CQT.zapoln_wtabl(self, rez, tbl, set_isp_nomera_col=0, separ='', isp_shapka=True,
                         set_editeble_col_nomera={nk_teg}, ogr_maxshir_kol=500)
        tbl.setColumnWidth(nk_zapis, int(tbl.width() * 0.7))
        tbl.hideColumn(nk_pnom)
        tbl.setColumnWidth(nk_teg, int(tbl.width() * 0.2))
        tbl.setColumnWidth(nk_stat, int(tbl.width() * 0.03))
        visota_stroki = 22
        for i in range(1, len(spis)):
            block = spis[i][nk_zapis].split('@')
            for j in range(len(block)):
                ur = block[j].split('|')[20]
                block[j] = [tab * int(ur) + block[j]]
                # tmp_block.append([tmp_str])
            tbl.setRowHeight(i - 1, visota_stroki)
            CQT.add_table(tbl, i - 1, nk_zapis, block, visota = int(visota_stroki/len(block)))
            CQT.add_check_box(tbl, i - 1, nk_stat, conn_func_checked_row_col=self.click_check)
            if tbl.item(i - 1, nk_stat).text() == '0':
                tbl.cellWidget(i - 1, nk_stat).setChecked(False)
                CQT.ust_color_row_wtab(tbl, i - 1, 211, 211, 211)
            else:
                tbl.cellWidget(i - 1, nk_stat).setChecked(True)
                CQT.ust_color_row_wtab(tbl, i - 1, 255, 255, 255)



    def click_check(self, stat, row, col):
        tbl = self.ui.tbl_magaz
        nk_stat = CQT.nom_kol_po_imen(tbl, 'Статус')
        if stat:
            tbl.item(row, nk_stat).setText('1')
            CQT.ust_color_row_wtab(tbl, row, 255, 255, 255)
        else:
            tbl.item(row, nk_stat).setText('0')
            CQT.ust_color_row_wtab(tbl, row, 211, 211, 211)

    def tbl_magaz_click(self):
        tbl = self.ui.tbl_magaz
        nk_stat = CQT.nom_kol_po_imen(tbl, 'Статус')
        row = tbl.currentRow()
        if tbl.currentColumn() == nk_stat:
            if tbl.cellWidget(row, tbl.currentColumn()).isChecked():
                tbl.cellWidget(row, tbl.currentColumn()).setChecked(False)
                tbl.item(row, nk_stat).setText('0')
                CQT.ust_color_row_wtab(tbl, row, 211, 211, 211)
            else:
                tbl.cellWidget(row, tbl.currentColumn()).setChecked(True)
                tbl.item(row, nk_stat).setText('1')
                CQT.ust_color_row_wtab(tbl, row, 255, 255, 255)

    def save_tk(self):
        osn_nadp = []
        n_dse = self.ui.lineEdit_dse
        naim_dse = self.ui.lineEdit_dse_naim
        n_tk = self.ui.lineEdit_nntk
        n_tk_km = self.ui.lineEdit_nntk_mat
        n_tk_es = self.ui.lineEdit_nntk_esk
        lit = self.ui.comboBox_liter
        razr = self.ui.lineEdit_razrab
        d_raz = self.ui.lineEdit_dat_raz
        prov = self.ui.lineEdit_prover
        norm = self.ui.lineEdit_normir
        metr = self.ui.lineEdit_metr_eksp
        nor_kont = self.ui.lineEdit_Norm_k
        prim = self.ui.lineEdit_Primech
        flag_etapi = True
        if naim_dse.text() == '':
            CQT.msgbox('Не заполнен наиенование ДСЕ')
            return
        if n_tk.text() == '':
            CQT.msgbox('Не заполнен номер технологической карты')
            return
        # if n_tk_km.text() == '':
        #    CQT.msgbox('Не заполнен номер карты материалов')
        # if n_tk_es.text() == '':
        #    CQT.msgbox('Не заполнен номер карты эскизов')
        if flag_etapi == False:
            if lit.currentText() == '-':
                CQT.msgbox('Не выбрана литера')
                return
            if prov.text() == '':
                CQT.msgbox('Не заполнена графа Проверил')
                return
            if norm.text() == '':
                CQT.msgbox('Не заполнена графа Нормировал')
                return
            if metr.text() == '':
                CQT.msgbox('Не заполнена графа Метрологическая эксп.')
                return
            if nor_kont.text() == '':
                CQT.msgbox('Не заполнена графа Нормоконтроль')
                return
        if razr.text() == '':
            CQT.msgbox('Не заполнена графа Разработчик')
            return
        if d_raz.text() == '':
            CQT.msgbox('Не заполнена графа Дата разработки')
            return
        osn_nadp.append(n_dse.text() + '$' + naim_dse.text())
        osn_nadp.append(n_tk.text() + '/' + n_tk_km.text() + '/' + n_tk_es.text())
        osn_nadp.append(lit.currentText())
        osn_nadp.append(razr.text())
        osn_nadp.append(d_raz.text())
        osn_nadp.append(prov.text())
        osn_nadp.append(norm.text())
        osn_nadp.append(metr.text())
        osn_nadp.append(nor_kont.text())
        osn_nadp.append(prim.text())

        telo = CQT.spisok_dreva(self.ui.tree)
        # if telo == []:
        #    return
        sp_soh = []
        for i in osn_nadp:
            sp_soh.append(i)
        for i in telo:
            sp_soh.append("|".join(i))

        ima = n_tk.text() + '_' + n_dse.text() + ".txt"
        if F.nalich_file(F.scfg("add_docs")) == False:
            F.sozd_dir(F.scfg("add_docs"))
        if 'по маршрутной карте' in self.windowTitle():
            nom_mk = self.windowTitle().split('карте ')[-1]
            F.zap_f(F.scfg('Naryad') + os.sep + nom_mk + os.sep + ima, sp_soh, pickl=True)
        else:
            F.zap_f(F.scfg("add_docs") + os.sep + ima, sp_soh, pickl=True)
            # self.export_csv_op(telo, n_dse.text(), naim_dse.text().replace('\n', ' '))  # запись csv по операциям
            if F.nalich_file(F.bdcfg('Naryad')) == False:
                CQT.msgbox('Не найдена БД')
                return
            # spis_BD = CSQ.spis_iz_bd_sql(F.bdcfg('Naryad'), 'dse', True,True)
            CSQ.update_bd_sql(F.bdcfg('Naryad'), 'dse',
                              {'Номер_техкарты': n_tk.text()},
                              {'Номенклатурный_номер': n_dse.text(), 'Наименование': naim_dse.text()})
            self.obnov_dse()
        tmp_flag_naid = False
        tmp_spis_mk = F.otkr_f('O:\Производство Powerz\Отдел технолога\ТД\МК_журнал.txt', separ='|')
        naim = F.ochist_strok_pod_ima_fila(naim_dse.text())
        spis_soh_list = [x.split('|') for x in sp_soh]
        self.load_param_from_dxf(spis_soh_list)
        try:
            for i in range(len(tmp_spis_mk)):
                if len(tmp_spis_mk[i]) > 2:
                    if tmp_spis_mk[i][2] == naim and tmp_spis_mk[i][1] == n_dse.text():
                        tmp_flag_naid = True
                        break
            if tmp_flag_naid == False:
                tmp_spis_mk.append(
                    [str(int(tmp_spis_mk[-1][0]) + 1), n_dse.text(), naim, '', '', '', '', '', F.now(), razr.text()])
                F.zap_f('O:\Производство Powerz\Отдел технолога\ТД\МК_журнал.txt', tmp_spis_mk, separ='|')
        except:
            pass
        return

    def tree_noma_vrem(self):
        tree = self.ui.tree
        item = tree.currentItem()
        kod = tree.currentItem().text(3)
        spisok = CQT.spisok_dreva(tree)
        if item == None:
            return
        obr = item.text(3)
        ur = item.text(20)
        if ur == "0":
            return
        flag = False
        for i in range(0, len(spisok)):
            if obr == spisok[i][3]:
                flag = True
                for j in range(i, 0, -1):
                    if 1 == int(spisok[j][20]):
                        metka = j
                        break
            if flag:
                break

        flag_vse = True
        flag_odna = False
        summ = 0
        for i in range(metka + 1, len(spisok)):
            if spisok[i][20] != '2':
                break

            if spisok[i][7] != "":
                spisok[i][7] = spisok[i][7].replace(',', '.')
                if F.is_numeric(spisok[i][7]):
                    flag_odna = True
                    summ += float(spisok[i][7])
                else:
                    flag_vse = False
            else:
                flag_vse = False

        if flag_vse:
            spisok[metka][7] = str(round(summ, 1))
            CQT.msgbox('Время штучное на ' + spisok[metka][2] + " операцию, успешно пересчитано")
        else:
            if flag_odna:
                spisok[metka][7] = '0'
                CQT.msgbox('Время штучное на ' + spisok[metka][
                    2] + " операцию, не рассчитано. Не заполнено время на все переходы")
        self.zapoln_tree_spiskom(spisok)
        CQT.videlit_tree_znach(self.ui.tree, 3, kod)

    def tree_del(self):
        rez = CQT.msgboxgYN('Точно удалить?')
        if rez == False:
            return
        tree = self.ui.tree
        item = tree.currentItem()
        spisok = CQT.spisok_dreva(tree)
        cur_str = self.ui.tree.currentItem().text(3)
        if item == None:
            return
        obr = item.text(3)
        ur = item.text(20)
        flag = False
        spisok_tmp = spisok.copy()
        for i in range(0, len(spisok)):
            if obr == spisok[i][3]:
                spisok_tmp.remove(spisok[i])
                flag = True
                for j in range(i + 1, len(spisok)):
                    if int(ur) < int(spisok[j][20]):
                        spisok_tmp.remove(spisok[j])
                    else:
                        break
            if flag:
                break
        self.zapoln_tree_spiskom(spisok_tmp)
        CQT.videlit_tree_znach(self.ui.tree, 3, cur_str, -1)

    def tree_paste(self):
        buf = self.ui.t_buff_0
        if self.ui.tree.currentItem() == None:
            cur_str = 'Т1'
        else:
            cur_str = self.ui.tree.currentItem().text(3)
        self.tree_paste_buf_n(buf)
        CQT.videlit_tree_znach(self.ui.tree, 3, cur_str)
        return

    def tree_copy(self):
        buf = self.ui.t_buff_0
        self.tree_copy_buf_n(buf)
        return

    def tree_paste_buf_n(self, obj):
        tree = self.ui.tree
        item = tree.currentItem()
        buf = obj
        if item == None:
            cur_str = ""
        else:
            cur_str = self.ui.tree.currentItem().text(3)
        spisok = CQT.spisok_dreva(tree)
        if item == None and len(spisok) != 0:
            return
        if buf.rowCount() == 0:
            return
        tmp = CQT.spisok_iz_wtabl(buf)
        if len(spisok) == 0:
            spisok = tmp
            self.zapoln_tree_spiskom(spisok)
            return
        tmp_ur = tmp[0][20]
        obr = item.text(3)
        ur = item.text(20)
        metka = len(spisok)
        flag = False
        for i in range(0, len(spisok)):
            if obr == spisok[i][3]:
                for j in range(i + 1, len(spisok)):
                    if int(tmp_ur) >= int(spisok[j][20]):
                        metka = j
                        flag = True
                        break
            if flag:
                break
        n = 0
        for i in range(len(tmp)):
            if tmp[i][20] == '1' or tmp[i][20] == '2':
                tmp[i][7] = '*'
            if tmp[i][20] == '1':
                tmp[i][10] = ''

            tmp[i][15] = ''
            tmp[i][1] = ''
            spisok.insert(metka + n, tmp[i])
            n += 1
        self.zapoln_tree_spiskom(spisok)
        CQT.videlit_tree_znach(self.ui.tree, 3, cur_str)

    def tree_copy_buf_n(self, obj):
        tree = self.ui.tree
        item = tree.currentItem()
        buf = obj
        if item == None:
            return
        obr = item.text(3)
        ur = item.text(20)
        tmp = []
        spisok = CQT.spisok_dreva(tree)
        for i in range(0, len(spisok)):
            if obr in spisok[i][3]:
                tmp.append("|".join(spisok[i]))
        isp_n_k = 0
        CQT.zapoln_wtabl(mywindow, tmp, buf, isp_n_k, 0, (), (), 200, False, "|", 5)
        return

    def resizeEvent(self, event):
        self.resized.emit()
        return super(mywindow, self).resizeEvent(event)

    def widths(self):
        tab_per_ins = self.ui.tap_per_insrt
        tab_per_ins.setColumnWidth(0, int(tab_per_ins.width()))
        tab_per_osn = self.ui.tap_per_osnast
        tab_per_osn.setColumnWidth(0, int(tab_per_osn.width()))
        tab3 = self.ui.tab_kar
        tab3.setColumnWidth(0, int(tab3.width() * 0.1))
        tab3.setColumnWidth(1, int(tab3.width() * 0.3))
        tab3.setColumnWidth(2, int(tab3.width() * 0.3))
        tab3.setColumnWidth(3, int(tab3.width() * 0.3) - 6)
        tab2 = self.ui.tap_per
        tab2.setColumnWidth(0, int(tab2.width() * 0.3))
        tab2.setColumnWidth(1, int(tab2.width() * 0.3))
        tab2.setColumnWidth(2, int(tab2.width() * 0.4) - 5)
        tabl = self.ui.tab_op
        tabl.setColumnWidth(0, int(tabl.width() * 0))
        tabl.setColumnWidth(1, int(tabl.width() * 0.05))
        tabl.setColumnWidth(2, int(tabl.width() * 0.2))
        tabl.setColumnWidth(4, int(tabl.width() * 0.3))
        tabl.setColumnWidth(5, int(tabl.width() * 0.05))
        tabl.setColumnWidth(6, int(tabl.width() * 0.05))
        tabl.setColumnWidth(7, int(tabl.width() * 0.05))
        tabl.setColumnWidth(8, int(tabl.width() * 0.05))
        tabl.setColumnWidth(9, int(tabl.width() * 0.05))
        tabl.setColumnWidth(4, int(tabl.width() - tabl.columnWidth(0) - tabl.columnWidth(1) - tabl.columnWidth(2)
                                   - tabl.columnWidth(3) - tabl.columnWidth(5) - tabl.columnWidth(6)
                                   - tabl.columnWidth(7) - tabl.columnWidth(8) - tabl.columnWidth(9)) - 5)
        tab_oper_mat = self.ui.tbl_oper_mat
        tab_oper_mat.setColumnWidth(0, int(tab_oper_mat.width() * 0.3))
        tab_oper_mat.setColumnWidth(1, int(tab_oper_mat.width() * 0.3))
        tab_oper_mat.setColumnWidth(2, int(tab_oper_mat.width() * 0.4))
        tab_oper_mat_red = self.ui.tableW_oper_mat
        tab_oper_mat_red.setColumnWidth(0, int(tab_oper_mat_red.width() * 0.1))
        tab_oper_mat_red.setColumnWidth(1, int(tab_oper_mat_red.width() * 0.7))
        tab_oper_mat_red.setColumnWidth(2, int(tab_oper_mat_red.width() * 0.1))
        tab_oper_mat_red.setColumnWidth(3, int(tab_oper_mat_red.width() * 0.1))
        tab_doc_tk = self.ui.tab_tk_doc
        tab_doc_tk.setColumnWidth(0, tab_doc_tk.width())
        tab_doc_op = self.ui.tab_op_doc
        tab_doc_op.setColumnWidth(0, tab_doc_op.width())

    def tree_vverh(self):
        tree = self.ui.tree

        tci = tree.currentItem()
        if tci == None:
            return
        obr = tci.text(3)
        ur = tci.text(20)
        rez = self.tree_move_vverh(obr, ur)
        CQT.videlit_tree_znach(tree, 3, rez)
        tree.setFocus(True)

    def tree_vniz(self):
        tree = self.ui.tree
        tci = tree.currentItem()
        obr = tci.text(3)
        ur = tci.text(20)
        spisok = CQT.spisok_dreva(tree)
        for i in range(0, len(spisok)):
            if spisok[i][3] == obr:
                nach = i
                break
        metka = None
        for i in range(nach + 1, len(spisok)):
            if spisok[i][20] == ur:
                metka = i
                break
            if int(spisok[i][20]) < int(ur):
                break
        if metka != None:
            obr = spisok[metka][3]
            ur = spisok[metka][20]
            rez = self.tree_move_vverh(obr, ur)
        CQT.videlit_tree_znach(tree, 3, rez)
        tree.setFocus(True)

    def tree_move_vverh(self, obr, ur):
        tree = self.ui.tree
        ci = tree.currentIndex().row()
        # obr = item.text(3)
        # ur = item.text(20)
        tmp = []
        spisok = CQT.spisok_dreva(tree)
        for i in range(0, len(spisok)):
            if spisok[i][3] == obr:
                nach = i
                break

        metka = None
        for i in range(nach - 1, -1, -1):
            if int(spisok[i][20]) < int(ur):
                return
            if spisok[i][20] == ur:
                metka = i
                break
        if metka == nach:
            return
        if metka == None:
            return

        for i in range(0, len(spisok)):
            if obr in spisok[i][3]:
                tmp.append(spisok[i])

        for i in range(0, len(tmp)):
            spisok.remove(tmp[i])

        for i in range(len(tmp) - 1, -1, -1):
            spisok.insert(metka, tmp[i])

        self.zapoln_tree_spiskom(spisok)
        # tree.itemAt(metka,0).setSelected(True)

        tree.selectionModel().select(tree.model().index(metka, 0),
                                     QtCore.QItemSelectionModel.Clear | QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        tree.selectionModel().setCurrentIndex(tree.model().index(metka, 0),
                                              QtCore.QItemSelectionModel.Clear | QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
        # treeWidget->selectionModel()->select(treeWidget->model()->index(row, 0),
        #                                                          QItemSelectionModel::SelectCurrent | QItemSelectionModel::Rows );
        # self.device_view.selectionModel().select(self.dev_model.index(0),
        #                                         QItemSelectionModel.Select)
        return spisok[metka][3]

    def zapoln_tree_spiskom(self, spisok):
        spisok = self.obnovit_numeraciy(spisok)
        tree = self.ui.tree
        tree.clear()
        n = 0
        for i in range(0, len(spisok)):
            if spisok[i][20] == '0':
                root = QtWidgets.QTreeWidgetItem(tree)
                tmp = root
            if spisok[i][20] == '1':
                root = QtWidgets.QTreeWidgetItem(tmp)
                tmp2 = root
            if spisok[i][20] == '2':
                root = QtWidgets.QTreeWidgetItem(tmp2)
            for j in range(0, len(spisok[i])):
                root.setText(j, spisok[i][j])
            tree.addTopLevelItem(root)
            tree.expandItem(root)
            n += 1
        try:
            tree.setCurrentItem(root)
        except:
            pass
        self.cveta_v_drevo(145, 218, 145, 255)
        self.load_shir_kol_tree()

    def opn_doc(self):
        tree = self.ui.tree
        item = tree.currentItem()
        if item == None:
            return
        if item.text(15) == "":
            return
        rez = db_files_load(item.text(15))
        if rez == False:
            CQT.msgbox(f'Файл {item.text(15)} не найден в бд')
            return
        F.zapyst_file(rez)

    def dob_doc(self):
        tree = self.ui.tree
        item = tree.currentItem()
        if item == None:
            return
        ima_det = self.windowTitle().split('$')[1]
        tmp_putt = CMS.load_tmp_path("tmp_addtk_doc")

        putf = CQT.f_dialog_name(self, 'Выбрать файл', tmp_putt, f"Файлы (*{ima_det.replace(' ','')}*.dxf *.jpg *.pdf)")
        if putf == '' or putf == '.':
            return
        CMS.save_tmp_path("tmp_addtk_doc", putf, True)
        file_name_bd = db_files_nalich(putf,self.nom_tk)
        r"""
        ima_f = putf.split(os.sep)[-1]
        new_ima = F.ubrat_rasshir(ima_f) + '_' + str(F.time_metka()) + F.ostavit_rasshir(ima_f)
        nputf = F.scfg('add_docs') + '\\' + new_ima
        rez = F.skopir_file(putf, nputf)"""

        try:
            item.setText(15, file_name_bd)
            item.setText(1, '...')
            CQT.msgbox("Файл прикреплен успешно")
            self.save_tk()
            return
        except:
            CQT.msgbox("Не удалось прикрепить файл")
            return

    def ydal_doc(self):
        tree = self.ui.tree
        item = tree.currentItem()
        if item == None:
            return
        if item.text(15) == "":
            return
        #F.udal_file(F.scfg('add_docs') + '//' + item.text(15))
        db_files_del(item.text(15),self.nom_tk)
        CQT.msgbox("Файл откреплен успешно")
        item.setText(15, "")
        item.setText(1, '')
        self.save_tk()
        return

    def click_tableW_oper_mat(self):
        tbl = self.ui.tableW_oper_mat

        _translate = QtCore.QCoreApplication.translate
        #tbl.setToolTipDuration()
        if tbl.currentItem() == None:
            return
        tbl.setToolTip(_translate("MainW", tbl.currentItem().text()))

    def zap_mat_v_tree(self):
        tab = self.ui.tableW_oper_mat
        tab_oper = self.ui.tbl_oper_mat
        if tab_oper.currentIndex().row() == -1:
            CQT.msgbox('Не выбрана операция')
            return
        nk_norm = CQT.nom_kol_po_imen(tab, 'Норма')
        if tab.rowCount() >= 0:
            strok = []
            for st in range(0, tab.rowCount()):
                podstrok = []
                if F.is_numeric(tab.item(st, nk_norm).text()) == False:
                    CQT.msgbox(f'В строке {st+1}  не число!')
                    return
                for i in range(0, tab.columnCount()):
                    if tab.item(st, i) == None:
                        CQT.msgbox("Не полностью заполенена запись")
                        return
                    tmp = F.ochist_strok_pod_separ(tab.item(st, i).text())
                    podstrok.append(tmp)
                strok.append('$'.join(podstrok))
            strok = '{'.join(strok)
            #nom_op = CQT.cells(tab_oper.currentIndex().row(), 0, tab_oper)
            nom_op = tab_oper.item(tab_oper.currentRow(),CQT.nom_kol_po_imen(tab_oper,'ID')).text()
            self.zapis_v_drevo(nom_op, 10, strok)
            CQT.msgbox('Записано успешно')


    def obnovit_mater_tabl(self):
        tab_oper = self.ui.tbl_oper_mat
        tab_oper_mat_red = self.ui.tableW_oper_mat
        if tab_oper.currentRow() == -1:
            return
        if tab_oper.item(tab_oper.currentRow(),CQT.nom_kol_po_imen(tab_oper,'ID')) == None:
            return
        id_op = tab_oper.item(tab_oper.currentRow(),CQT.nom_kol_po_imen(tab_oper,'ID')).text()
        if id_op == None:
            return
        slov_op = self.slovar_drev(1, id_op)
        tab_oper_mat_red.clearContents()
        tab_oper_mat_red.setRowCount(0)

        n = 0
        for i in slov_op.keys():
            spis_k = slov_op[i]
            spis_strok_mat = spis_k[10].split('{')
            if spis_strok_mat[0] == '' and len(spis_strok_mat) == 1:
                return
            tab_oper_mat_red.setRowCount(len(spis_strok_mat))
            for i in range(0, len(spis_strok_mat)):
                spis_mat = spis_strok_mat[i].split('$')
                for j in range(0, len(spis_mat)):
                    cellinfo = QtWidgets.QTableWidgetItem(spis_mat[j])
                    tab_oper_mat_red.setItem(i, j, cellinfo)
        tab_oper_mat_red.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def sozd_file(self,nom_mk):
        self.load_redaktor_tk(nom_mk)
        n_dse = self.ui.lineEdit_dse
        n_tk = self.ui.lineEdit_nntk
        n_tk_km = self.ui.lineEdit_nntk_mat
        n_tk_es = self.ui.lineEdit_nntk_esk
        lit = self.ui.comboBox_liter
        razr = self.ui.lineEdit_razrab
        d_raz = self.ui.lineEdit_dat_raz
        prov = self.ui.lineEdit_prover
        norm = self.ui.lineEdit_normir
        metr = self.ui.lineEdit_metr_eksp
        nor_kont = self.ui.lineEdit_Norm_k
        prim = self.ui.lineEdit_Primech
        naim_dse = self.ui.lineEdit_dse_naim
        tbl_dse = self.ui.tblw_dse
        nom_kol_nom_tk = CQT.nom_kol_po_imen(tbl_dse, 'Номер_техкарты')
        if self.ui.pushButton_sozd.text() == 'Создать':
            if len(n_tk.text()) < 7:
                CQT.msgbox(f'Номер техкарты короткий')
                return
        n_k_nn = CQT.nom_kol_po_imen(tbl_dse, 'Номенклатурный_номер')
        n_k_naim = CQT.nom_kol_po_imen(tbl_dse, 'Наименование')
        if tbl_dse.item(tbl_dse.currentRow(), n_k_nn) != None:
            if n_dse.text() != tbl_dse.item(tbl_dse.currentRow(), n_k_nn).text():
                n_dse.setText(tbl_dse.item(tbl_dse.currentRow(), n_k_nn).text())
        if tbl_dse.item(tbl_dse.currentRow(), n_k_nn) != None:
            if naim_dse.text() != tbl_dse.item(tbl_dse.currentRow(), n_k_naim).text():
                naim_dse.setText(tbl_dse.item(tbl_dse.currentRow(), n_k_naim).text())

        rez = self.block_tk(naim_dse.text(), n_dse.text())
        if rez != True:
            CQT.msgbox(f'Техкарта на редактировании {rez}')
            self.ui.pushButton_sozd.setEnabled(False)
            return
        else:
            self.ui.pushButton_sozd.setEnabled(True)

        flag_etapi = True
        if n_dse.text() == '' and naim_dse.text() == "":
            CQT.msgbox('Не заполнен номер, название ДСЕ')
            return
        if naim_dse.text() == "":
            CQT.msgbox('Не заполнен название ДСЕ')
            return
        if n_tk.text() == '':
            CQT.msgbox('Не заполнен номер технологической карты')
            return
        # if n_tk_km.text() == '':
        #    CQT.msgbox('Не заполнен номер карты материалов')
        # if n_tk_es.text() == '':
        #    CQT.msgbox('Не заполнен номер карты эскизов')

        if razr.text() == '':
            CQT.msgbox('Не заполнена графа Разработчик')
            return
        if d_raz.text() == '':
            CQT.msgbox('Не заполнена графа Дата разработки')
            return
        if flag_etapi == False:
            if lit.currentText() == '-':
                CQT.msgbox('Не выбрана литера')
                return
            if prov.text() == '':
                CQT.msgbox('Не заполнена графа Проверил')
                return
            if norm.text() == '':
                CQT.msgbox('Не заполнена графа Нормировал')
                return
            if metr.text() == '':
                CQT.msgbox('Не заполнена графа Метрологическая эксп.')
                return
            if nor_kont.text() == '':
                CQT.msgbox('Не заполнена графа Нормоконтроль')
                return

        self.ui.tab_kar.setRowCount(0)
        self.ui.tab_tk_doc.setRowCount(0)
        self.ui.tab_op.setRowCount(0)
        self.ui.tab_op_doc.setRowCount(0)
        self.ui.tap_per.setRowCount(0)
        #CQT.zapoln_vtabl(self, self.ui.tableV_oper_mat, ["||"], "|", True)

        # self.ui.tableV_oper_mat.reset()
        self.ui.tableW_oper_mat.setRowCount(0)
        if self.ui.pushButton_sozd.text() == 'Изменить':
            self.save_tk()
        else:
            # ogr_rezhim = self.nalichie_nevip_mk(n_dse.text(), naim_dse.text())
            self.setWindowTitle(n_tk.text() + '$' + n_dse.text() + "$" + naim_dse.text())
            self.nom_tk = n_tk.text()
            self.dse_nn = n_dse.text()
            self.dse_naim = naim_dse.text()
        self.ui.tabWidget.setTabEnabled(1, True)
        self.ui.tabWidget.setCurrentIndex(1)


    def load_redaktor_tk(self,po_mk):
        tabl_bd = self.ui.tblw_dse
        prim_dse = CQT.cells(tabl_bd.currentIndex().row(), CQT.nom_kol_po_imen(tabl_bd, 'Примечание'), tabl_bd)
        if po_mk == False:
            self.ui.pushButton_Vverh.setEnabled(True)
            self.ui.pushButton_Vniz.setEnabled(True)
            self.ui.pushButton_Copy.setEnabled(True)
            self.ui.pushButton_Paste.setEnabled(True)
            self.ui.pushButton_Del.setEnabled(True)
        self.ui.tree.clear()
        self.zagr_tk(po_mk)
        self.ui.lbl_primech_dse.setText(prim_dse)

    def load_zagolovok_dse(self,po_mk):
        tabl_bd = self.ui.tblw_dse
        nom_dse = CQT.cells(tabl_bd.currentIndex().row(), 0, tabl_bd)
        nom_tk = CQT.cells(tabl_bd.currentIndex().row(), 2, tabl_bd)
        nom_nazv = CQT.cells(tabl_bd.currentIndex().row(), 1, tabl_bd)


        le_n_dse = self.ui.lineEdit_dse
        le_n_tk = self.ui.lineEdit_nntk
        le_naim_dse = self.ui.lineEdit_dse_naim
        le_n_tk_km = self.ui.lineEdit_nntk_mat
        le_n_tk_es = self.ui.lineEdit_nntk_esk
        le_n_dse.setText(nom_dse)
        le_naim_dse.setText(nom_nazv)
        self.ui.lbl_marsh.setText('')
        lit = self.ui.comboBox_liter
        razr = self.ui.lineEdit_razrab
        d_raz = self.ui.lineEdit_dat_raz
        prov = self.ui.lineEdit_prover
        norm = self.ui.lineEdit_normir
        metr = self.ui.lineEdit_metr_eksp
        nor_kont = self.ui.lineEdit_Norm_k
        prim = self.ui.lineEdit_Primech

        le_n_tk.clear()
        lit.setCurrentIndex(0)
        razr.clear()
        d_raz.clear()
        prov.clear()
        norm.clear()
        metr.clear()
        nor_kont.clear()
        prim.clear()
        le_n_tk_km.clear()
        le_n_tk_es.clear()
        self.ui.pushButton_sozd.setEnabled(True)
        if self.ui.tabWidget_2.currentIndex() == CQT.nom_tab_po_imen(self.ui.tabWidget_2, 'ЦП'):
            self.ui.axWidget.dynamicCall('Navigate(const QString&)', "")
        CQT.clear_tbl(self.ui.tbl_isp_mk)
        if nom_tk != '':
            self.ui.pushButton_sozd.setText('Изменить')
            le_n_tk.setText(nom_tk)
            le_n_dse.setEnabled(False)
            le_n_tk.setEnabled(False)
            le_naim_dse.setEnabled(False)
        else:
            # self.ui.pushButton_zagruz.setEnabled(False)
            self.ui.pushButton_sozd.setText('Создать')
            self.ui.lineEdit_razrab.setText(os.environ.get("USERNAME"))
            self.ui.lineEdit_dat_raz.setText(F.date())
            le_n_dse.setEnabled(True)
            le_n_tk.setEnabled(True)
            le_naim_dse.setEnabled(True)
            if nom_dse == '':
                le_n_tk.setText(f'ТДТК.{F.ochist_strok_pod_ima_fila(nom_nazv)}')
            else:
                le_n_tk.setText(f'ТДТК.{nom_dse}')
            le_n_tk_km.setText('ТДКМ')
            self.setWindowTitle('')
            self.nom_tk = ''
            self.dse_nn = ""
            self.dse_naim = ""
        ima = nom_tk + '_' + nom_dse + ".txt"
        if po_mk == False:
            spisok_tk = F.otkr_f(F.scfg("add_docs") + os.sep + ima, False, '|', pickl=True, propuski=True)

            self.setWindowTitle(nom_tk + '$' + nom_dse + "$" + nom_nazv)
        else:
            spisok_tk = F.otkr_f(F.scfg("Naryad") + os.sep + po_mk + os.sep + ima, False, '|', pickl=True, propuski=True)
            self.setWindowTitle(
                nom_tk + '$' + nom_dse + "$" + nom_nazv + "$по маршрутной карте " + po_mk)

        if spisok_tk == ['']:
            return
        self.nom_tk = nom_tk
        self.dse_nn = nom_dse
        self.dse_naim = nom_nazv
        marshrut = []
        flag_naid = False
        for i in range(10, len(spisok_tk)):
            if spisok_tk[i][20] == '1':
                marshrut.append(spisok_tk[i][4])
            if spisok_tk[i][20] == '0':
                if flag_naid:
                    break
                flag_naid = True

        self.ui.lbl_marsh.setText('-->'.join(marshrut))
        if self.ui.tabWidget_2.currentIndex() == CQT.nom_tab_po_imen(self.ui.tabWidget_2, 'ЦП'):
            if len(spisok_tk) > 10 and 'фровая подпи' in spisok_tk[10][15]:
                # CQT.msgbox(f'Документ подписан {spisok_tk[10][15]}')
                # self.WebBrowser = self.ui.axWidget
                self.ui.axWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.ui.axWidget.setControl("{8856F961-340A-11D0-A96B-00C04FD705A2}")
                rez = db_files_load(spisok_tk[10][15])
                if rez:
                    f = Path(rez).as_uri()
                    self.ui.axWidget.dynamicCall('Navigate(const QString&)', f)

        nn, nazv = [x for x in spisok_tk[0][0].split('$')]
        le_n_dse.setText(nn)
        le_naim_dse.setText(nazv)
        tk, km, es = [x for x in spisok_tk[1][0].split('/')]
        le_n_tk.setText(tk)
        le_n_tk_km.setText(km)
        le_n_tk_es.setText(es)
        lit.setCurrentText(spisok_tk[2][0])
        razr.setText(spisok_tk[3][0])
        d_raz.setText(spisok_tk[4][0])
        prov.setText(spisok_tk[5][0])
        norm.setText(spisok_tk[6][0])
        metr.setText(spisok_tk[7][0])
        nor_kont.setText(spisok_tk[8][0])
        prim.setText(spisok_tk[9][0])

    def vibor_dse(self, po_mk=False):
        self.load_zagolovok_dse(po_mk)





    def save_shir_kol_tree(self):
        tree = self.ui.tree
        arr_shir = []
        for i in range(tree.columnCount()):
            arr_shir.append(tree.columnWidth(i))
        if F.nalich_file(CMS.tmp_dir()) == False:
            F.sozd_dir(CMS.tmp_dir())
        F.zap_f(CMS.tmp_dir() + os.sep + 'shir_kol_tree.txt', arr_shir, separ='', pickl=True)

    def load_shir_kol_tree(self):
        tree = self.ui.tree
        if F.nalich_file(CMS.tmp_dir() + os.sep + 'shir_kol_tree.pickle'):
            arr = F.otkr_f(CMS.tmp_dir() + os.sep + 'shir_kol_tree.txt', pickl=True)
            for i in range(len(arr)):
                tree.setColumnWidth(i, int(arr[i]))

    def obnovit_param_tablic(self):
        tree = self.ui.tree
        item = tree.currentItem()
        if item == None:
            return
        uroven = item.text(20)
        self.ui.tab_op.clearContents()
        self.ui.tab_op.setRowCount(0)
        self.ui.tap_per.clearContents()
        self.ui.tap_per.setRowCount(0)
        self.ui.tap_per_insrt.clearContents()
        self.ui.tap_per_insrt.setRowCount(0)
        self.ui.tap_per_osnast.clearContents()
        self.ui.tap_per_osnast.setRowCount(0)
        self.cvet_knopki()
        if uroven == "0":
            self.obnovit_param_tabl_kar(item)
            self.obnovit_param_tabl_kar_doc(item)
            self.obnovit_param_tabl_oper_mat()
        if uroven == "1":
            self.obnovit_param_tabl_oper_doc(item)
            self.obnovit_param_tabl_oper()
            self.obnovit_param_tabl_kar(item.parent())
            self.obnovit_param_tabl_oper_mat()
            self.obnovit_param_tabl_kar_doc(item.parent())
        if uroven == "2":
            self.obnovit_param_tabl_oper_doc(item.parent())
            self.obnovit_param_tabl_oper()
            self.obnovit_param_tabl_kar(item.parent().parent())
            self.obnovit_param_tabl_kar_doc(item.parent().parent())
            self.obnovit_param_tabl_pereh()

    def obnovit_param_tabl_oper_mat(self):
        tab_oper_mat = self.ui.tbl_oper_mat
        if self.ui.tree.currentItem() == None:
            return
        par = self.ui.tree.currentItem().parent()
        if par == None:
            kod_par = self.ui.tree.currentItem().text(3)
        else:
            kod_par = par.text(3)
        slov_op = self.slovar_drev(1, kod_par)
        spisok_zn_op = []
        spisok_zn_op.append('ID' + "|" + 'Номер' + "|" + 'Операция')
        n = 0
        for i in slov_op.keys():
            spis_k = slov_op[i]
            spisok_zn_op.append(spis_k[3] + "|" + spis_k[2] + "|" + spis_k[0])
        #CQT.zapoln_vtabl(self, tab_oper_mat, spisok_zn_op, "|", True)
        CQT.zapoln_wtabl(self,spisok_zn_op,tab_oper_mat,separ='|',isp_shapka=True)
        tab_oper_mat.resizeColumnsToContents()
        tab_oper_mat.horizontalHeader().setStretchLastSection(True)

    def obnovit_param_tabl_pereh(self):
        tabl = self.ui.tap_per
        tabl_osn = self.ui.tap_per_osnast
        tabl_ins = self.ui.tap_per_insrt
        par = self.ui.tree.currentItem()
        kod_par = par.text(3)
        slov_per = self.slovar_drev(2, kod_par)
        tabl.clearContents()
        tabl.setRowCount(len(slov_per))
        tabl_osn.clearContents()
        tabl_osn.setRowCount(9)
        tabl_ins.clearContents()
        tabl_ins.setRowCount(9)
        n = 0
        for i in slov_per.keys():
            spis_k = slov_per[i]
            cellinfo = QtWidgets.QTableWidgetItem(spis_k[3])
            tabl.setItem(n, 0, cellinfo)
            cellinfo = QtWidgets.QTableWidgetItem(spis_k[2])
            tabl.setItem(n, 1, cellinfo)
            cellinfo = QtWidgets.QTableWidgetItem(spis_k[7])
            tabl.setItem(n, 2, cellinfo)
            for j in range(4, 3):
                cellinfo = QtWidgets.QTableWidgetItem(spis_k[j])
                tabl.setItem(n, j - 1, cellinfo)
            s_osn = spis_k[11].split('$')
            for j in range(0, len(s_osn)):
                cellinfo = QtWidgets.QTableWidgetItem(s_osn[j])
                tabl_osn.setItem(j, 0, cellinfo)
            s_ins = spis_k[12].split('$')
            for j in range(0, len(s_ins)):
                cellinfo = QtWidgets.QTableWidgetItem(s_ins[j])
                tabl_ins.setItem(j, 0, cellinfo)
            n += 1
        for i in range(0, tabl_osn.rowCount()):
            tabl_osn.setRowHeight(i, 18)
        for i in range(0, tabl_ins.rowCount()):
            tabl_ins.setRowHeight(i, 18)
        tabl_osn.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tabl_ins.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tabl.horizontalHeader().setStretchLastSection(True)
        tabl.resizeColumnsToContents()
        tabl.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def obnovt_drevo_s_tabl1_op(self):
        tree = self.ui.tree
        tabl = self.ui.tab_op
        tabl_doc = self.ui.tab_op_doc
        if self.ui.tree.currentItem() == None:
            CQT.msgbox('Не выполнено')
            return
        cur_str = self.ui.tree.currentItem().text(3)
        if tabl.rowCount() == 0:
            return

        for i in range(0, tabl.rowCount()):
            tabl.item(i, 5).setText(tabl.item(i, 5).text().replace(',', '.'))
            tabl.item(i, 6).setText(tabl.item(i, 6).text().replace(',', '.'))
            if self.flag_proverka_op:
                if F.is_numeric(tabl.item(i, 5).text().strip()) == False:
                    CQT.msgbox('Тпз не число')
                    tabl.setCurrentCell(i, 5)
                    return
                if F.is_numeric(tabl.item(i, 6).text().strip()) == False and tabl.item(i, 6).text() != '*':
                    CQT.msgbox('Тшт не число')
                    tabl.setCurrentCell(i, 6)
                    return
                if F.is_numeric(tabl.item(i, 7).text().strip()) == False:
                    CQT.msgbox('Код профессии не число')
                    tabl.setCurrentCell(i, 7)
                    return
                if F.is_numeric(tabl.item(i, 8).text().strip()) == False:
                    CQT.msgbox('Кол-во исполнителей не число')
                    tabl.setCurrentCell(i, 8)
                    return
                if F.is_numeric(tabl.item(i, 9).text().strip()) == False:
                    CQT.msgbox('КОИД не число')
                    tabl.setCurrentCell(i, 9)
                    return
                if F.valm(tabl.item(i, 5).text().strip()) == 0:
                    CQT.msgbox('В операциях не может Тпз равно 0 ' + tabl.item(i, 1).text().strip())
                    return
                if F.valm(tabl.item(i, 8).text().strip()) > 2:
                    CQT.msgbox('В операциях не может быть больше двух исполнителей ' + tabl.item(i, 1).text().strip())
                    return

        for i in range(0, tabl.rowCount()):
            for j in range(3, tabl.columnCount() - 1):
                self.zapis_v_drevo(tabl.item(i, 0).text(), j + 1, F.ochist_strok_pod_separ(tabl.item(i, j).text()))
            self.zapis_v_drevo(tabl.item(i, 0).text(), 11, F.ochist_strok_pod_separ(tabl.item(i, 9).text()))

        if tree.currentItem().text(20) == '2':
            obr = tree.currentItem().parent().text(3)
        if tree.currentItem().text(20) == '1':
            obr = tree.currentItem().text(3)

        s_doc = []
        for i in range(0, tabl_doc.rowCount()):
            if tabl_doc.item(i, 0) != None:
                s_doc.append(F.ochist_strok_pod_separ(tabl_doc.item(i, 0).text()))
        self.zapis_v_drevo(obr, 13, '$'.join(s_doc))

        self.save_tk()
        CQT.ust_cvet_obj(self.ui.Button_t_op)
        CQT.videlit_tree_znach(self.ui.tree, 3, cur_str)

    def obnovt_drevo_s_tabl3_kar(self):
        tabl = self.ui.tab_kar
        tabl_doc = self.ui.tab_tk_doc
        if self.ui.tree.currentItem() == None:
            return
        cur_str = self.ui.tree.currentItem().text(3)

        iskl_sp = []
        if tabl.rowCount() == 0:
            return
        for i in range(0, tabl.rowCount()):
            for j in range(1, tabl.columnCount()):
                if j not in iskl_sp:
                    self.zapis_v_drevo(tabl.item(i, 0).text(), j + 4, F.ochist_strok_pod_separ(tabl.item(i, j).text()))
        s_doc = []
        for i in range(0, tabl_doc.rowCount()):
            if tabl_doc.item(i, 0) != None:
                s_doc.append(F.ochist_strok_pod_separ(tabl_doc.item(i, 0).text()))
        self.zapis_v_drevo(tabl.item(0, 0).text(), 13, '$'.join(s_doc))

        self.save_tk()
        CQT.ust_cvet_obj(self.ui.Button_t_kar)
        CQT.videlit_tree_znach(self.ui.tree, 3, cur_str)

    def obnovt_drevo_s_tab2_per(self):
        tabl = self.ui.tap_per
        tabl_osn = self.ui.tap_per_osnast
        tabl_ins = self.ui.tap_per_insrt
        cur_str = self.ui.tree.currentItem().text(3)

        if tabl.rowCount() == 0:
            return
        for i in range(0, tabl.rowCount()):
            tabl.item(i, 2).setText(tabl.item(i, 2).text().replace(',', '.'))
            self.zapis_v_drevo(tabl.item(i, 0).text(), 7, F.ochist_strok_pod_separ(tabl.item(i, 2).text()))
            self.zapis_v_drevo(tabl.item(i, 0).text(), 4, '')
        s_osn = []
        for i in range(0, tabl_osn.rowCount()):
            if tabl_osn.item(i, 0) != None:
                s_osn.append(F.ochist_strok_pod_separ(tabl_osn.item(i, 0).text()))
        self.zapis_v_drevo(tabl.item(0, 0).text(), 11, '$'.join(s_osn))

        s_ins = []
        for i in range(0, tabl_ins.rowCount()):
            if tabl_ins.item(i, 0) != None:
                s_ins.append(F.ochist_strok_pod_separ(tabl_ins.item(i, 0).text()))
        self.zapis_v_drevo(tabl.item(0, 0).text(), 12, '$'.join(s_ins))
        self.tree_noma_vrem()
        self.save_tk()
        CQT.ust_cvet_obj(self.ui.Button_t_per)
        # index = self.ui.tree.model().index()
        CQT.videlit_tree_znach(self.ui.tree, 3, cur_str)
        # self.ui.tree.selectionModel().setCurrentIndex(index, QtCore.QItemSelectionModel.NoUpdate)

    def zapis_v_drevo(self, ID, kol, item):
        it = QtWidgets.QTreeWidgetItemIterator(self.ui.tree)
        while it.value():
            currentItem = it.value()
            if currentItem.text(3) == str(ID):
                currentItem.setText(kol, item)
                return
            it += 1

    def cveta_v_drevo(self, r, g, b, a):
        it = QtWidgets.QTreeWidgetItemIterator(self.ui.tree)
        while it.value():
            currentItem = it.value()
            if currentItem.parent() == None:
                obr = currentItem.text(2)
                while it.value():
                    currentItem = it.value()
                    if obr in currentItem.text(3):
                        for _ in range(0, 3):
                            currentItem.setBackground(_, QtGui.QColor(r, g, b, a))
                    it += 1
                return
            it += 1

    def obnovit_param_tabl_kar_doc(self, obj):
        tabl_doc = self.ui.tab_tk_doc
        tabl_doc.clearContents()
        tabl_doc.setRowCount(9)
        s_doc = obj.text(13).split('$')
        for j in range(0, len(s_doc)):
            cellinfo = QtWidgets.QTableWidgetItem(s_doc[j])
            tabl_doc.setItem(j, 0, cellinfo)
        for i in range(0, tabl_doc.rowCount()):
            tabl_doc.setRowHeight(i, 18)
        # tabl_doc.resizeColumnsToContents()
        # tabl_doc.horizontalHeader().setStretchLastSection(True)
        tabl_doc.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def obnovit_param_tabl_kar(self, item):
        tabl = self.ui.tab_kar
        if item == None:
            return
        spis = []
        spis.append(item.text(3))
        for i in range(5, 8):
            spis.append(item.text(i))
        tabl.clearContents()
        tabl.setRowCount(1)
        n = 0
        for i in spis:
            cellinfo = QtWidgets.QTableWidgetItem(i)
            tabl.setItem(0, n, cellinfo)
            n += 1
        # tabl.resizeColumnsToContents()
        # tabl.horizontalHeader().setStretchLastSection(True)
        tabl.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def obnovit_param_tabl_oper_doc(self, obj):
        tabl_doc = self.ui.tab_op_doc
        tabl_doc.clearContents()
        tabl_doc.setRowCount(9)
        s_doc = obj.text(13).split('$')
        for j in range(0, len(s_doc)):
            cellinfo = QtWidgets.QTableWidgetItem(s_doc[j])
            tabl_doc.setItem(j, 0, cellinfo)
        for i in range(0, tabl_doc.rowCount()):
            tabl_doc.setRowHeight(i, 18)
        # tabl_doc.resizeColumnsToContents()
        # tabl_doc.horizontalHeader().setStretchLastSection(True)
        tabl_doc.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def obnovit_param_tabl_oper(self):
        tabl = self.ui.tab_op
        par = self.ui.tree.currentItem().parent()
        if par == None:
            return
        kod_par = par.text(3)
        slov_op = self.slovar_drev(1, kod_par)
        tabl.clearContents()
        tabl.setRowCount(len(slov_op))
        n = 0
        for i in slov_op.keys():
            spis_k = slov_op[i]
            cellinfo = QtWidgets.QTableWidgetItem(spis_k[3])
            tabl.setItem(n, 0, cellinfo)
            cellinfo = QtWidgets.QTableWidgetItem(spis_k[2])
            tabl.setItem(n, 1, cellinfo)
            cellinfo = QtWidgets.QTableWidgetItem(spis_k[0])
            tabl.setItem(n, 2, cellinfo)
            for j in range(4, 10):
                cellinfo = QtWidgets.QTableWidgetItem(spis_k[j])
                if self.ogr_rezim():
                    if j == 4:
                        cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                tabl.setItem(n, j - 1, cellinfo)
            cellinfo = QtWidgets.QTableWidgetItem(spis_k[11])
            tabl.setItem(n, 9, cellinfo)
            n += 1
        tabl.resizeColumnsToContents()
        tabl.horizontalHeader().setStretchLastSection(True)

    def spisok(self):
        self.slovar_drev()

    def slovar_drev(self, uroven='xxx', kod_par=''):
        spisok = {}
        it = QtWidgets.QTreeWidgetItemIterator(self.ui.tree)
        while it.value():
            currentItem = it.value()

            if uroven == 'xxx':
                sp = []
                for i in range(0, currentItem.columnCount()):
                    sp.append(currentItem.text(i))
                spisok[currentItem.text(3)] = sp
            if uroven == 0:
                if currentItem.text(currentItem.columnCount() - 1) == "0":
                    sp = []
                    for i in range(0, currentItem.columnCount()):
                        sp.append(currentItem.text(i))
                    spisok[currentItem.text(3)] = sp
            if uroven == 1:
                if currentItem.text(currentItem.columnCount() - 1) == "1":
                    if kod_par in currentItem.text(3):
                        sp = []
                        for i in range(0, currentItem.columnCount()):
                            sp.append(currentItem.text(i))
                        spisok[currentItem.text(3)] = sp
            if uroven == 2:
                if currentItem.text(currentItem.columnCount() - 1) == "2":
                    if kod_par in currentItem.text(3):
                        sp = []
                        for i in range(0, currentItem.columnCount()):
                            sp.append(currentItem.text(i))
                        spisok[currentItem.text(3)] = sp

            if currentItem.childCount() == 0:
                if currentItem.checkState(0) == 0:
                    pass
            it += 1
        if uroven == 'xxx':
            for i in spisok.keys():
                # print(i + ' - ' + ','.join(spisok[i]))
                pass
        return spisok

    def sost(self):
        it = QtWidgets.QTreeWidgetItemIterator(self.ui.tree)
        while it.value():
            currentItem = it.value()
            print('-------------')
            for i in range(0, currentItem.columnCount() + 1):
                print(currentItem.text(i), end='|')
            if currentItem.childCount() == 0:
                if currentItem.checkState(0) == 0:
                    pass
            print('')
            it += 1

    def rnd_frase(self):
        sp = F.otkr_f(F.scfg('cash') + os.sep + 'frase.txt')
        if sp != [''] and len(sp) > 0:
            if random.random() > 0.8:
                msgg = sp[random.randint(1, len(sp) - 1)]
                CQT.msgbox(msgg)

    def dobav_V_tree_root(self, strok):
        tree = self.ui.tree
        root = QtWidgets.QTreeWidgetItem(tree)
        root.setText(0, 'Техкарта ' + str(strok))
        root.setText(1, '')
        root.setText(2, 'Т' + str(strok))
        root.setText(3, 'Т' + str(strok))
        root.setText(5, F.date())
        root.setText(6, os.environ.get("USERNAME"))
        root.setText(20, '0')
        # root.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        tree.addTopLevelItem(root)
        tree.setCurrentItem(root)
        self.cveta_v_drevo(145, 218, 145, 255)
        self.w2 = mywindow2(tree, "Древо")
        self.w2.showNormal()
        self.w2.ui2.lineEdit.setText(self.ui.tree.currentItem().text(0))
        self.w2.ui2.lineEdit.setFocus()

    def zagruzka_shablona_operacii(self, child, PUT_K_TMP):
        putf = PUT_K_TMP + os.sep + "shablon_op.txt"
        if F.nalich_file(putf):
            spis = F.otkr_f(putf, separ='|')
            for i in range(1, len(spis)):
                if spis[i][0] == child.text(0):
                    if child.text(4).strip() == '':
                        child.setText(4, spis[i][1])
                    if child.text(5).strip() == '':
                        child.setText(5, spis[i][2])
                    if child.text(8).strip() == '':
                        child.setText(8, spis[i][3])
                    if child.text(13).strip() == '':
                        child.setText(13, spis[i][4]) if len(spis[i]) > 4 else None
                    break
            return child
        return child

    def dobav_V_tree_oper(self, item="", uroven=""):
        tree = self.ui.tree
        if item == "":
            item = tree
        strok = item.childCount()
        child1 = QtWidgets.QTreeWidgetItem(item)
        child1.setText(0, 'Операция')
        zap_strok = '0' * (3 - len(str((strok + 1) * 5))) + str((strok + 1) * 5)
        child1.setText(1, '')
        child1.setText(2, zap_strok)
        child1.setText(3, uroven + '-' + zap_strok)
        child1.setText(9, '1')
        child1.setText(11, '1')
        child1.setText(20, '1')

        # root.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        tree.addTopLevelItem(child1)
        tree.expandItem(item)
        tree.setCurrentItem(child1)
        self.cveta_v_drevo(145, 218, 145, 255)
        self.w2 = mywindow2(tree, "Древо")
        self.w2.showNormal()
        self.w2.ui2.lineEdit.setText(self.ui.tree.currentItem().text(0))
        # self.w2.ui2.lineEdit.setFocus()

    def dobav_V_tree_perex(self, item="", uroven=""):
        tree = self.ui.tree
        # root = QtWidgets.QTreeWidgetItem(tree)

        if item == "":
            item = tree
        por_nom = item.childCount() + 1
        child1 = QtWidgets.QTreeWidgetItem(item)
        child1.setText(0, 'Переход')
        child1.setText(1, '')
        child1.setText(2, str(por_nom))
        child1.setText(3, uroven + '-' + str(por_nom))
        child1.setText(20, '2')
        # root.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        tree.addTopLevelItem(child1)
        tree.expandItem(item)
        tree.setCurrentItem(child1)
        self.cveta_v_drevo(145, 218, 145, 255)
        self.w2 = mywindow2(tree, "Древо")
        self.w2.showNormal()
        self.w2.ui2.lineEdit.setText(self.ui.tree.currentItem().text(0))
        self.w2.ui2.lineEdit.setFocus()

    def obnovit_numeraciy(self, spisok):
        t = 0
        for i in range(0, len(spisok)):
            if spisok[i][20] == "0":
                t += 1
                o = 0
                spisok[i][2] = "Т" + str(t)
                spisok[i][3] = "Т" + str(t)

            if spisok[i][20] == "1":
                o += 1
                p = 0
                zap_op = '0' * (3 - len(str(o * 5))) + str(o * 5)
                spisok[i][2] = zap_op
                spisok[i][3] = "Т" + str(t) + "-" + zap_op

            if spisok[i][20] == "2":
                p += 1
                zap_per = str(p)
                spisok[i][2] = zap_per
                spisok[i][3] = "Т" + str(t) + "-" + zap_op + "-" + zap_per
        return spisok

    def sohran_buff(self, nom, tabl):
        item = tabl
        stroki = CQT.spisok_iz_wtabl(item, '|')
        if F.nalich_file(self.PUT_K_TMP) == False:
            F.sozd_dir(self.PUT_K_TMP)
        puttf = self.PUT_K_TMP + os.sep + str(nom) + ".txt"
        F.zap_f(puttf, stroki)


# if not F.test_path():
#    exit()

rootitem1 = QtGui.QStandardItem('QAbstractItemView')

app = QtWidgets.QApplication(sys.argv)

args = sys.argv[1:]

myappid = 'Powerz.BAG.SustControlWork.0.0.0'  # !!!
'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'

#=============================================================
versia = '2.2.06'
if F.is_frozen()== False:
    if CMS.kontrol_ver(versia,'Техкарты') == False:
        quit()
#=============================================================

QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
app.setWindowIcon(QtGui.QIcon(os.path.join("icons", "icon.png")))
print(QtWidgets.QStyleFactory.keys())
S = F.scfg('Stile').split(",")
app.setStyle(S[1])

#==== БД файлов
db_files_create()

application = mywindow()
application.show()


sys.exit(app.exec())
# pyinstaller.exe --onefile --icon=1.ico --noconsole TehKart.py
# pyinstaller.exe --onefile --icon=1.ico TehKart.py


