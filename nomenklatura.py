# coding=cp1251
import pythoncom
import win32com.client
import Cust_SQLite as CSQ
import Cust_Functions as F

# import Cust_Qt as CQT

#if __name__ == '__main__':
#    exit()

SPIS_VIDOV = [
    '����� �������������',
    '����� � ����� ���������',
    '����� ��������',
    '����� ������',
    '���-�����',
    '����� ��',
    '�������',
    '��������� ��������',
    '���������������� ��������',
    '������',
    '���� �����',
    '����� (���� �2,�4)',
    '���� (���� �2,�4)',
    '����� (10,01)',
    '����� ���� 4032 DIN934',
    '����� ����������� ���� 11860',
    '����� ������ ���� 4035 DIN439',
    '����� ��� ��������� ���������� ���� 9064',
    '����� ���������� ���� 5918 (DIN935)',
    '������ ������������ (������) (10,01)',
    '�����',
    '��������',
    '������������ �����������',
    '������',
    '��������',
    '������',
    '��������',
    '�������������� ��������',
    '��������� ��������',
    '������',
    '�������',
    '������ ������������',
    '������ ��������������',
    '�������',
    '������� ���� 481-80',
    '��������� ���� 15180-86',
    '��������� ��� ���� 52376-2005',
    '��������� �� 5728-006-93978201-2008',
    '������������ ��������� (10,01)',
    '����������',
    '�����',
    '����� ���� 9941-81 (����)',
    '����� ���������� (10,01)',
    '����� �� ���� (10,01)',
    '����� �� �� (10,01)',
    '�������  ���� 22042',
    '������� ���� 9066 (��� �������)',
    '������� ��� ��������� ���������� ���� 9066',
    '������� DIN 975',
    '�����-����� (10,01)',
    '������� (10,01)',
    '��������-������� � ����������������� (10.01)',
    '��������� ��������� (10.01)',
    '���������� ������ ��������� (10.01)',
    '������� (10.01)',
    '�������� ����� (10.01)',
    '������ (10,01)',
    '������� (10,01)',
    '����� (10,01)',
    '�������� ������ (10,01)',
    '�������� (10,01)',
    '�������� (10.01)',
    '��������� ��� ��� (10,01)',
    '������������ (10.01)',
    '������������� ������ �� �������� �� ����� (10.01)',
    '������������� ��������� (10,01)',
    '�����',
    '������������ (10,01)',
    '���������� (10,01)',
    '������� (10,01)',
    '������ (10.01)',
    '������� (10.01)',
    '������ (10,01)',
    '��������� ��������� (10,01)',
    '�����',
    '��������� ������ (10.01)',
    '������ (10,01)',
    '������',
    '����� (10,01)',
    '������� (10,01)',
    '������������ (10,01)',
    '������ (10,01)',
    '������ (10.01)',
    '��������� (10.01)',
]
DICT_POLE = {
    '�������� ������ (10,01)': {
        '�1': '�������',
        '�2': '�����',
        '�3': '������',
        '�4': '���������',
        '�5': '���������',
        '�6': '���_���_cam',
    },
    '������� ���� 481-80': {
        '�1': '�������',
        '�2': '�����',
        '�3': '������',
        '�4': '���������',
        '�5': '���������',
    },
    '������ (10,01)': {
        '�1': '�������',
        '�2': '�����',
        '�3': '���������',
        '�4': '���������',
    },
    '����� (10,01)': {
        '�1': '�������',
        '�2': '�����',
        '�3': '���������',
        '�4': '���������',
    },
    '����� ���� 9941-81 (����)': {
        '�1': '�������',
        '�2': '���.�������',
        '�3': '��.�������',
        '�4': '���������',
        '�5': '���������',
        '�6': '����� �����',
    },
    '����� ���������� (10,01)': {
        '�1': '�������',
        '�2': '������',
        '�3': '������',
        '�4': '����� �����',
        '�5': '���������',
        '�6': '���������',
    },
    '����� �� ���� (10,01)': {
        '�1': '�������',
        '�2': '���.�������',
        '�3': '��.�������',
        '�4': '���������',
        '�5': '���������',
        '�6': '����� �����',
    },
    '����� �� �� (10,01)': {
        '�1': '�������',
        '�2': '���.�������',
        '�3': '��.�������',
        '�4': '���������',
        '�5': '���������',
        '�6': '����� �����',
    },
    '������� (10,01)': {
        '�1': 'b-������ �����',
        '�2': 's-������� ������',
        '�3': 't-������� �����',
        '�4': 'h-������ �����',
        '�5': '����� ��������',
        '�6': '���������',
        '�7': '���������',
    },
    '������ (10,01)': {
        '�1': '�������',
        '�2': 'a-������',
        '�3': 'b-������',
        '�4': '����� ������',
        '�5': '���������',
        '�6': '���������',
    },
    '������� (10,01)': {
        '�1': 's-������� ����������� �������',
        '�2': '����� ��������',
        '�3': '���������',
        '�4': '���������',
    },
    '������� (10,01)':{
        '�1':'s-������� ����������� �������',
        '�2':'����� ��������',
        '�3':'���������',
        '�4':'���������',
    },
    '������������ (10,01)':{
        '�1':'d�������� ��������� ����������',
        '�2':'����� �������������',
        '�3':'���������',
        '�4':'���������',
    }
}


def check_db(spis_izm):
    # spis_vidov_bd = [F.to_snake_notation(_) for _ in SPIS_VIDOV]
    if F.nalich_file(F.scfg('cash') + F.sep() + 'nomenklatura_erp.db') == False:
        frase_tmp = """CREATE TABLE IF NOT EXISTS nomen(
               ������ INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE ON CONFLICT ROLLBACK,
               ��� TEXT,
               ��� TEXT,
               ������� TEXT,
               ������������ TEXT,
               ���������������� TEXT,
               ��_�������� INTEGER,
               ����_��������� TEXT,
               ���������� TEXT,
               �1 TEXT,
               �2 TEXT,
               �3 TEXT,
               �4 TEXT,
               �5 TEXT,
               �6 TEXT,
               �7 TEXT);
            """
        CSQ.sozd_bd_sql(F.scfg('cash') + F.sep() + 'nomenklatura_erp.db', frase_tmp)
        spis_izm.append(['��', '������� �����'])
    for vid in SPIS_VIDOV:
        put = F.sep().join([F.scfg('cash'), 'bd_mater', f'{vid}.txt'])
        if F.nalich_file(put):
            print('We are testing columns in ' + put)
            spis_tex_param = F.otkr_f(put, separ='|', utf8=True)
            nk_kod = F.nom_kol_po_im_v_shap(spis_tex_param, '���')
            if nk_kod == None:
                print(f'�� {put} �� ������� ������� ���')
                return False
            for key in DICT_POLE.keys():
                if vid == key:
                    for key2 in DICT_POLE[key]:
                        nk = F.nom_kol_po_im_v_shap(spis_tex_param, DICT_POLE[key][key2])
                        if nk == None:
                            print(f'���������� ������� {DICT_POLE[key][key2]} � {key}')
                            return False
            print('         .... OK')
            print('')


def query_run_unify(V83, querytxt):
    query = V83.NewObject("Query", querytxt)
    return query.Execute().Choose()


def connect():
    print('Try connect to ERP')
    print(F.user_name())
    put_f = F.scfg('cash') + F.sep() + 'users_erp.txt'
    if F.nalich_file(put_f) == False:
        return '�� ����� ���� � ������� ������������� ���'
    print("���� ������")
    spis_users = F.otkr_f(put_f,True,separ='|')
    login = ''
    password = ''
    for i in range(len(spis_users)):
        if spis_users[i][0] == F.user_name():
            print("������������ ������")
            login = spis_users[i][1]
            password = spis_users[i][2]
            break
    if login == '' or password == '':
        return '�� ������ �����/������'
    #V83_CONN_STRING = 'Srvr="novgorod";Ref="ERP";Usr="������� ����� �����������";Pwd="25012022";'
    V83_CONN_STRING = f'Srvr="novgorod";Ref="ERP";Usr="{login}";Pwd="{password}";'
    print(f'���� {V83_CONN_STRING}')
    pythoncom.CoInitialize()
    V83 = win32com.client.Dispatch("V83.COMConnector").Connect(V83_CONN_STRING)
    print('         .... OK')
    print('')
    return V83


def query_mat(mat, V83):
    # get = lambda obj,attr: getattr(obj, str(attr.encode('cp1251', 'ignore')))
    # catalog = getattr(V83.Catalogs, "���������.��������������")
    spis = [["rez.���", "rez.�������", "rez.������������", "rez.����������������", "rez.���������������"]]
    query_mat = f'''�������
        ������������.��������������� ��� ���������������,
        ������������.������������ ��� ������������,
        ������������.������� ��� �������,
        ������������.����������������.������������ ��� ����������������,
        ������������.��� ��� ���
    ��
        ����������.������������ ��� ������������
    ���
        ������������.���������������.������������ = "{mat}"'''

    rez = query_run_unify(V83, query_mat)
    while rez.next():
        print(rez.���, rez.�������, rez.������������, rez.����������������, rez.���������������)
        spis.append([rez.���, rez.�������, rez.������������, rez.����������������, rez.���������������])
    return spis

def synchron_zapis(rez,vid,spis_izm,kod,table,i,conn,nk_art,nk_naim,nk_edizm):
    vid_old = rez[-1][F.nom_kol_po_im_v_shap(rez, '���')]
    if vid_old != vid:
        spis_izm.append([kod, f"{kod}, ����: {vid_old}, �����: {vid}"])
        zapros = f'''
                                                    UPDATE nomen SET ��� == '{vid}', ����_��������� == '{F.now()}' WHERE ��� == "{kod}"
                                                    '''
        CSQ.zapros('', zapros=zapros, conn=conn)

    art_old = rez[-1][F.nom_kol_po_im_v_shap(rez, '�������')]
    if art_old != table[i][nk_art]:
        spis_izm.append([kod, f"{kod}, ����: {art_old}, �����: {table[i][nk_art]}"])
        zapros = f'''
                                                    UPDATE nomen SET ������� == '{table[i][nk_art]}', ����_��������� == '{F.now()}' WHERE ��� == "{kod}"
                                                    '''
        CSQ.zapros('', zapros=zapros, conn=conn)

    naim_old = rez[-1][F.nom_kol_po_im_v_shap(rez, '������������')]
    if naim_old != table[i][nk_naim]:
        spis_izm.append([kod, f"{kod}, ����: {naim_old}, �����: {table[i][nk_naim]}"])
        zapros = f'''
                                                    UPDATE nomen SET ������������ == '{table[i][nk_naim]}', ����_��������� == '{F.now()}' WHERE ��� == "{kod}"
                                                    '''
        CSQ.zapros('', zapros=zapros, conn=conn)

    edizm_old = rez[-1][F.nom_kol_po_im_v_shap(rez, '����������������')]
    if edizm_old != table[i][nk_edizm]:
        spis_izm.append([kod, f"{kod}, ����: {edizm_old}, �����: {table[i][nk_edizm]}"])
        zapros = f'''
                                                    UPDATE nomen SET ������������ == '{table[i][nk_edizm]}', ����_��������� == '{F.now()}' WHERE ��� == "{kod}"
                                                    '''
        CSQ.zapros('', zapros=zapros, conn=conn)

def synchron_param(kod, vid, conn, cur, spis_izm, rez=''):
    put = F.sep().join([F.scfg('cash'), 'bd_mater', f'{vid}.txt'])
    if F.nalich_file(put):
        spis_tex_param = F.otkr_f(put, separ='|', utf8=True)
        nk_kod = F.nom_kol_po_im_v_shap(spis_tex_param, '���')
        stroka = ''
        for i in range(len(spis_tex_param)):
            if spis_tex_param[i][nk_kod] == kod:
                stroka = i
                break
        if stroka == '':
            return
        if vid not in DICT_POLE:
            print(f'�� ������ {vid} � �������')
            spis_izm.append(["������", f'�� ������ {vid} � �������'])
            return
        for key in DICT_POLE[vid].keys():
            nk = F.nom_kol_po_im_v_shap(spis_tex_param, DICT_POLE[vid][key])
            znach = spis_tex_param[stroka][nk]
            if rez != '':
                znach_old = rez[-1][F.nom_kol_po_im_v_shap(rez, key)]
            if rez == '' or znach != znach_old:
                zapros = f'''
                            UPDATE nomen SET {key} == '{znach}', ����_��������� == '{F.now()}' WHERE ��� == "{kod}"
                            '''
                CSQ.zapros('', zapros=zapros, conn=conn)
                spis_izm.append([kod, f"{key}, ����: {znach_old}, �����: {znach}"])

def general():
    spis_izm = []
    if check_db(spis_izm) == False:
        return '������'
    try:
        conn = connect()
        if type(conn) is type('123'):
            return conn
    except:
        return 'Unable connect, EXIT'

    DB_NOMEN = F.scfg('cash') + F.sep() + 'nomenklatura_erp.db'

    conn_db, cur_db = CSQ.connect_bd(DB_NOMEN)
    for vid in SPIS_VIDOV:
        table = query_mat(vid, conn)
        nk_kod = F.nom_kol_po_im_v_shap(table, "rez.���")
        nk_art = F.nom_kol_po_im_v_shap(table, "rez.�������")
        nk_naim = F.nom_kol_po_im_v_shap(table, "rez.������������")
        nk_edizm = F.nom_kol_po_im_v_shap(table, "rez.����������������")
        nk_udal = F.nom_kol_po_im_v_shap(table, "rez.���������������")
        for i in range(1, len(table)):

            kod = table[i][nk_kod]
            query = f"""
            SELECT * FROM nomen WHERE ��� == "{kod}"
            """
            rez = CSQ.zapros('', query, conn_db)
            if len(rez) > 1:
                print(f'�������� {kod}')
                synchron_zapis(rez,vid,spis_izm,kod,table,i,conn,nk_art,nk_naim,nk_edizm)
                synchron_param(kod, vid, conn_db, cur_db, spis_izm, rez)  # ��� ����
            else:
                strok_input = [vid,
                               table[i][nk_kod],
                               table[i][nk_art],
                               table[i][nk_naim],
                               table[i][nk_edizm],
                               table[i][nk_udal],
                               F.now(),
                               '',
                               '',
                               '',
                               '',
                               '',
                               '',
                               '',
                               '']
                CSQ.dob_strok_v_bd_sql(DB_NOMEN, 'nomen', [strok_input], conn=conn_db, cur=cur_db)
                spis_izm.append([table[i][nk_kod], '��������'])
                synchron_param(kod, vid, conn_db, cur_db, spis_izm)
    if spis_izm != []:
        put_f = F.putt_k_isp_file() + F.now('%d.%m.%Y') + '_��������� ���.txt'
        F.zap_f(put_f, spis_izm, separ='|')
        F.zapyst_file(put_f)
    return True

#general()