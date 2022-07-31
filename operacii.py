import Cust_Functions as F

if __name__ == 's__main__':
    exit()

def vremya_tsht_perehodi(ima_operacii,ima_perehoda, arr_tmp, arr_tmp_parent):
    vrema = 0
    if ima_operacii == 'Фрезерная':
        if ima_perehoda == 'Фрезеровать плоскость с точностью _,глубиной _, длиной _':
            vrema = frezerovnie_ploskosti(ima_operacii,ima_perehoda , arr_tmp, arr_tmp_parent)
        if ima_perehoda == 'Фрезеровать уступ глубиной  _, длиной  _, шириной  _ и фрезой диаметром  _':
            vrema = frezerovnie_ustupa(ima_operacii, ima_perehoda, arr_tmp, arr_tmp_parent)
        if ima_perehoda == 'Установить деталь _ переустановить деталь _ снять деталь':
            vrema = vspomogatelnoe(ima_operacii, ima_perehoda, arr_tmp, arr_tmp_parent)
        if ima_perehoda == 'Фрезеровать шпоночный паз на глубину  _, длиной  _':
            vrema = frezerovnie_shponki(ima_operacii, ima_perehoda, arr_tmp, arr_tmp_parent)
    return round(vrema, 3)

def frezerovnie_shponki(ima_operacii, ima_perehoda, arr_tmp, arr_tmp_parent):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';'}
    material = arr_tmp_parent[0]
    koef_mater = 1 if material == '1' else 1.2

    for key in slov_zamen.keys():
        arr_tmp[1][0] = arr_tmp[1][0].replace(key, slov_zamen[key])
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])

    arr_glubin_frezer = arr_tmp[1][0].split(";")
    arr_dlina_frezer = arr_tmp[1][1].split(";")
    summa_vremeni = 0

    if len(arr_glubin_frezer) == len(arr_dlina_frezer):
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + ima_perehoda + F.sep() + 'table1.txt'

        for i in range(len(arr_glubin_frezer)):
            glubin_frezer = F.valm(arr_glubin_frezer[i])
            dlina_frezer = F.valm(arr_dlina_frezer[i])
            vremya_shtuchnoe = table(putf, glubin_frezer, dlina_frezer)
            summa_vremeni += vremya_shtuchnoe
    else:
        return 0
    return summa_vremeni * 1.13 * koef_mater


def vspomogatelnoe(ima_operacii, ima_perehoda, arr_tmp, arr_tmp_parent):
    putf = F.scfg(
        'cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + ima_perehoda + F.sep() + 'table1.txt'
    massa = F.valm(arr_tmp[-1][0])
    kol_vo_povorotov = F.valm(arr_tmp[-1][1])
    tabl_parametr = table(putf, massa)
    Nvr = tabl_parametr * (1 + 0.8 * kol_vo_povorotov)
    return Nvr


def frezerovnie_ustupa(ima_operacii, ima_perehoda, arr_tmp, arr_tmp_parent):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';'}
    material = arr_tmp_parent[0]
    koef_mater = 1 if material == '1' else 1.2

    for key in slov_zamen.keys():
        arr_tmp[1][0] = arr_tmp[1][0].replace(key, slov_zamen[key])
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])
        arr_tmp[1][2] = arr_tmp[1][2].replace(key, slov_zamen[key])
        arr_tmp[1][3] = arr_tmp[1][3].replace(key, slov_zamen[key])

    arr_glubin_frezer = arr_tmp[1][0].split(";")
    arr_dlina_frezer = arr_tmp[1][1].split(";")
    arr_shirina_frezer = arr_tmp[1][2].split(";")
    arr_diametr_frez = arr_tmp[1][3].split(";")
    summa_vremeni = 0

    if len(arr_glubin_frezer) == len(arr_dlina_frezer) == len(arr_shirina_frezer) == len(arr_diametr_frez):
        putf_chern = F.scfg(
            'cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + ima_perehoda + F.sep() + 'table1.txt'

        for i in range(len(arr_glubin_frezer)):
            glubin_frezer = F.valm(arr_glubin_frezer[i])
            dlina_frezer = F.valm(arr_dlina_frezer[i])
            shirina_frezer = F.valm(arr_shirina_frezer[i])
            diametr_frez = F.valm(arr_diametr_frez[i])
            shirina_hoda = 0

            if glubin_frezer <= 0.3 * diametr_frez:
                shirina_hoda = diametr_frez
            elif glubin_frezer <= 0.5 * diametr_frez:
                shirina_hoda = 0.7 * diametr_frez
            elif glubin_frezer <= 0.7 * diametr_frez:
                shirina_hoda = 0.5 * diametr_frez 
            elif glubin_frezer <= diametr_frez:
                shirina_hoda = 0.3 * diametr_frez
            elif glubin_frezer <= 2 * diametr_frez:
                shirina_hoda = 0.1 * diametr_frez

            dlina_hoda = dlina_frezer * (1 + shirina_frezer // shirina_hoda) + diametr_frez
            vremya_za_hod_chern = table(putf_chern, dlina_hoda)
            vremya_za_hod = vremya_za_hod_chern

            if (dlina_hoda > 950):
                vremya_za_hod += ((dlina_hoda - 950) // 100 + 1) * 2.15

            chislo_hodov = glubin_frezer // 30 + 1
            vremya_shtuchnoe = vremya_za_hod * chislo_hodov

            summa_vremeni += vremya_shtuchnoe
    else:
        return 0
    summa_vremeni *= 1.25 * koef_mater
    return summa_vremeni


def frezerovnie_ploskosti(ima_operacii, ima_perehoda, arr_tmp, arr_tmp_parent):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';'}
    material = arr_tmp_parent[0]
    koef_mater = 1 if material == '1' else 1.2

    for key in slov_zamen.keys():
        arr_tmp[1][0] = arr_tmp[1][0].replace(key, slov_zamen[key])
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])
        arr_tmp[1][2] = arr_tmp[1][2].replace(key, slov_zamen[key])

    arr_tochnost = arr_tmp[1][0].split(";")
    arr_glubin_frezer = arr_tmp[1][1].split(";")
    arr_dlina_frezer = arr_tmp[1][2].split(";")
    summa_vremeni = 0

    if len(arr_glubin_frezer) == len(arr_dlina_frezer):
        putf_chern = F.scfg(
            'cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + ima_perehoda + F.sep() + 'table1.txt'
        putf_poluchist = F.scfg(
            'cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + ima_perehoda + F.sep() + 'table2.txt'

        for i in range(len(arr_glubin_frezer)):
            glubin_frezer = F.valm(arr_glubin_frezer[i])
            dlina_frezer = F.valm(arr_dlina_frezer[i])

            vremya_za_hod_chern = table(putf_chern, dlina_frezer)
            chislo_hodov = 1 + glubin_frezer // 5
            vremya_za_hod = vremya_za_hod_chern

            if (dlina_frezer > 950):
                vremya_za_hod +=  (1 + (dlina_hoda - 950) // 100) * 0.9

            vremya_shtuchnoe = vremya_za_hod * chislo_hodov

            if (arr_tochnost[i] == '2'):
                vremya_za_hod_poluchist = table(putf_poluchist, dlina_hoda)
                if (dlina_frezer > 950):
                    vremya_za_hod_poluchist += (1 + (dlina_hoda - 950) // 100) * 0.77
                vremya_shtuchnoe += vremya_za_hod_poluchist

            summa_vremeni += vremya_shtuchnoe

    else:
        return 0
    summa_vremeni *= 1.2 * koef_mater
    return summa_vremeni


def vremya_tsht(ima_operacii, arr_tmp):
    vrema = 0
    if ima_operacii == 'Вальцовка':
        vrema = valcovka(ima_operacii, arr_tmp)
    if ima_operacii == 'Гибка':
        vrema = gibka(ima_operacii, arr_tmp)
    if ima_operacii == 'Сборка общая':
        vrema = sbor_obsh(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(зачистка швов)':
        vrema = sles_zach_shvov(ima_operacii, arr_tmp)
    if ima_operacii == 'Сборка под сварку':
        vrema = sb_pod_sv(ima_operacii, arr_tmp)
    if ima_operacii == 'Гравировальная':
        vrema = gravir(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(снять заусенцы)':
        vrema = sles_zausenci(ima_operacii, arr_tmp)
    if ima_operacii == 'Отрезка(гильотина)':
        vrema = gilotina(ima_operacii, arr_tmp)
    if ima_operacii == 'Окрашивание':
        vrema = okras(ima_operacii, arr_tmp)
    if ima_operacii == 'Отрезка(лентопил)':
        vrema = otrez_lentopil(ima_operacii, arr_tmp)
    if ima_operacii == 'Сварка':
        vrema = svarka(ima_operacii, arr_tmp)
    if ima_operacii == 'Сборка линз':
        vrema = sborka_linz(ima_operacii, arr_tmp)
    if ima_operacii == 'Укладка набивки':
        vrema = ukladka_nabivki(ima_operacii, arr_tmp)
    if ima_operacii == 'Формовка линз':
        vrema = formovka_linz(ima_operacii, arr_tmp)
    if ima_operacii == 'Отрезка слесарная':
        vrema = otrez_sles(ima_operacii, arr_tmp)
    if ima_operacii == 'Дробеструйная':
        vrema = drobestrui(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(правка в плоскости)':
        vrema = sles_prav(ima_operacii, arr_tmp)
    if ima_operacii == 'Сверлильная':
        vrema = sverlil(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(сверление)':
        vrema = sles_sverl(ima_operacii, arr_tmp)
    if ima_operacii == 'Штамповочная(перфорация)':
        vrema = shtamp_perf(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(нарезка резьбы)':
        vrema = sles_rezba(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(разделка кромок)':
        vrema = sles_razd_krom(ima_operacii, arr_tmp)
    if ima_operacii == 'Кантование':
        vrema = kantovanie(ima_operacii, arr_tmp)
    if ima_operacii == 'Резка(ЧПУ)':
        vrema = lazer(ima_operacii, arr_tmp)
    if ima_operacii == 'Вальцовка линз':
        vrema = valtcovka_linz(ima_operacii, arr_tmp)
    if ima_operacii == 'Комплектовочная':
        vrema = komplektov(ima_operacii, arr_tmp)
    if ima_operacii == 'Перемещение':
        vrema = peremeschenie(ima_operacii, arr_tmp)
    if ima_operacii == 'Контроль(формы и расположения поверхностей)':
        vrema = kontrol_form_i_raspoloj_poverhn(ima_operacii, arr_tmp)
    if ima_operacii == 'Контроль(механическая обработка)':
        vrema = kontrol_mech_obrabot(ima_operacii, arr_tmp)
    if ima_operacii == 'Контрольная цветная деффектоскопия':
        vrema = kontrol_tcvet_defekt(ima_operacii, arr_tmp)
    if ima_operacii == 'Рейкодолбежная':
        vrema = reykodolbejnaya(ima_operacii, arr_tmp)
    return round(vrema, 2)


def materiali(ima_operacii, arr_tmp):
    mat = ""
    if ima_operacii == 'Вальцовка':
        mat = komp_valcovka(ima_operacii, arr_tmp)
    if ima_operacii == 'Отрезка(лентопил)':
        mat = komp_otrezka_lentopil(ima_operacii, arr_tmp)
    if ima_operacii == 'Отрезка(гильотина)':
        mat = komp_gilotina(ima_operacii, arr_tmp)
    if ima_operacii == 'Токарная':
        mat = komp_tokarnaya(ima_operacii, arr_tmp)
    if ima_operacii == 'Сборка под сварку':
        mat = komp_sb_pod_sv(ima_operacii, arr_tmp)
    if ima_operacii == 'Фрезерная':
        mat = komp_frezernaya(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(нарезка резьбы)':
        mat = komp_sles_rezba(ima_operacii, arr_tmp)
    if ima_operacii == 'Резка(ЧПУ)':
        mat = komp_lazernaya_rezka(ima_operacii, arr_tmp)
    if ima_operacii == 'Вальцовка линз':
        mat = komp_valtcovka_linz(ima_operacii, arr_tmp)
    if ima_operacii == 'Гибка':
        mat = komp_gibka(ima_operacii, arr_tmp)
    if ima_operacii == 'Гравировальная':
        mat = komp_gravirov(ima_operacii, arr_tmp)
    if ima_operacii == 'Комплектовочная':
        mat = komp_komplektov(ima_operacii, arr_tmp)
    if ima_operacii == 'Отрезка слесарная':
        mat = komp_otrezka_slesar(ima_operacii, arr_tmp)
    if ima_operacii == 'Перемещение':
        mat = komp_peremeschenie(ima_operacii, arr_tmp)
    if ima_operacii == 'Рейкодолбежная':
        mat = komp_reykodolbejnaya(ima_operacii, arr_tmp)
    if ima_operacii == 'Сборка линз':
        mat = komp_sborka_linz(ima_operacii, arr_tmp)
    if ima_operacii == 'Сборка общая':
        mat = komp_sborka_obschaya(ima_operacii, arr_tmp)
    if ima_operacii == 'Сварка':
        mat = komp_svarka(ima_operacii, arr_tmp)
    if ima_operacii == 'Сверлильная':
        mat = komp_sverlilnaya(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(зачистка швов)':
        mat = komp_slesarnaya_zach_shvov(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(правка в плоскости)':
        mat = komp_slesarnya_pravka_v_plos(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(сверление)':
        mat = komp_slesarnaya_sverlen(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(снять заусенцы)':
        mat = komp_slesarnaya_snyatie_zausentcev(ima_operacii, arr_tmp)
    if ima_operacii == 'Укладка набивки':
        mat = komp_ukladka_nabivki(ima_operacii, arr_tmp)
    if ima_operacii == 'Формовка линз':
        mat = komp_formovka_linz(ima_operacii, arr_tmp)
    if ima_operacii == 'Штамповочная(перфорация)':
        mat = komp_shtampovochnaya(ima_operacii, arr_tmp)
    if ima_operacii == 'Слесарная(разделка кромок)':
        mat = komp_slesarnaya_razdelka_kromok(ima_operacii, arr_tmp)
    if ima_operacii == 'Кантование':
        mat = komp_kantovanie(ima_operacii, arr_tmp)
    if ima_operacii == 'Контроль(формы и расположения поверхностей)':
        mat = komp_kontrol_form_i_raspoloj_poverhn(ima_operacii, arr_tmp)
    if ima_operacii == 'Контроль(механическая обработка)':
        mat = komp_kontrol_mech_obrabot(ima_operacii, arr_tmp)
    if ima_operacii == 'Контрольная цветная деффектоскопия':
        mat = komp_kontrol_tcvet_defekt(ima_operacii, arr_tmp)
    if ima_operacii == 'Резка плазма':
        mat = komp_rezka_plazma(ima_operacii, arr_tmp)
    tmp = []
    for i in range(len(mat)):
        tmp.append('$'.join(mat[i]))
    return '{'.join(tmp)


def komp_rezka_plazma(ima_operacii, arr_tmp):
    vrema = rezka_plazma(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_kontrol_tcvet_defekt(ima_operacii, arr_tmp):
    vrema = kontrol_tcvet_defekt(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_kontrol_mech_obrabot(ima_operacii, arr_tmp):
    vrema = kontrol_mech_obrabot(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_kontrol_form_i_raspoloj_poverhn(ima_operacii, arr_tmp):
    vrema = kontrol_form_i_raspoloj_poverhn(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_kantovanie(ima_operacii, arr_tmp):
    vrema = kantovanie(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_slesarnaya_razdelka_kromok(ima_operacii, arr_tmp):
    vrema = sles_razd_krom(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_shtampovochnaya(ima_operacii, arr_tmp):
    vrema = shtamp_perf(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_formovka_linz(ima_operacii, arr_tmp):
    vrema = formovka_linz(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_ukladka_nabivki(ima_operacii, arr_tmp):
    vrema = ukladka_nabivki(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_slesarnaya_snyatie_zausentcev(ima_operacii, arr_tmp):
    vrema = sles_zausenci(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_slesarnaya_sverlen(ima_operacii, arr_tmp):
    vrema = sles_sverl(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_slesarnya_pravka_v_plos(ima_operacii, arr_tmp):
    vrema = sles_prav(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_slesarnaya_zach_shvov(ima_operacii, arr_tmp):
    vrema = sles_zach_shvov(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_sverlilnaya(ima_operacii, arr_tmp):
    vrema = sverlil(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_svarka(ima_operacii, arr_tmp):
    vrema = svarka(ima_operacii, arr_tmp)
    mat = arr_tmp[1][0]
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table7.txt'
    plotn = F.valm(table(putf, mat))

    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';', 'c': 'с', 'C': 'С', 'T': 'Т'}
    for key in slov_zamen.keys():
        arr_tmp[1][5] = arr_tmp[1][5].replace(key, slov_zamen[key])
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])
        arr_tmp[1][2] = arr_tmp[1][2].replace(key, slov_zamen[key])
        arr_tmp[1][3] = arr_tmp[1][3].replace(key, slov_zamen[key])



    koef_arr = arr_tmp[1][5].split(";")  # число отверстий
    vid_shva_arr = arr_tmp[1][1].split(";")  # Диаметр отверстий
    dl_arr = arr_tmp[1][2].split(";")  # Число пазов
    tolsh_arr = arr_tmp[1][3].split(";")  # толщина


    spis_prov = []
    for i in range(len(koef_arr)):
        nr_prov = 0
        tolsh = F.valm(tolsh_arr[i])
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table5.txt'
        kod_prov = table(putf, mat, tolsh,False)
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table8.txt'
        naim_prov = table(putf, kod_prov, rez_valm=False)
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table9.txt'
        edizm_prov = table(putf, kod_prov,rez_valm=False)
        koef_sl = koef_arr[i]
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table2.txt'
        koef_sl_rez = F.valm(table(putf, koef_sl))
        vid_shva = vid_shva_arr[i]
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table4.txt'
        pl_pop_sech = F.valm(table(putf, vid_shva))*tolsh
        dlina = F.valm(dl_arr[i])
        nr_prov += koef_sl_rez*pl_pop_sech*plotn*dlina/1000000
        spis_prov.append([kod_prov, naim_prov, edizm_prov, str(round(nr_prov,8))])

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis_prov.append([spis[i][0],spis[i][1],spis[i][2],str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))])
    return spis_prov


def komp_sborka_obschaya(ima_operacii, arr_tmp):
    vrema = sbor_obsh(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_sborka_linz(ima_operacii, arr_tmp):
    vrema = sborka_linz(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_reykodolbejnaya(ima_operacii, arr_tmp):
    vrema = reykodolbejnaya(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_peremeschenie(ima_operacii, arr_tmp):
    vrema = peremeschenie(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_otrezka_slesar(ima_operacii, arr_tmp):
    vrema = otrez_sles(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_kontrol(ima_operacii, arr_tmp):
    pass


def komp_komplektov(ima_operacii, arr_tmp):
    vrema = komplektov(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_gravirov(ima_operacii, arr_tmp):
    vrema = gravir(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_tokarnaya(ima_operacii, arr_tmp):
    vrema = tokarnaya(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_lazernaya_rezka(ima_operacii, arr_tmp):
    vrema = lazer(ima_operacii, arr_tmp)
    obor = str(arr_tmp[1][2])
    if obor == '0':
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    else:
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table2.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_valtcovka_linz(ima_operacii, arr_tmp):
    vrema = valtcovka_linz(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_gibka(ima_operacii, arr_tmp):
    vrema = gibka(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_sles_rezba(ima_operacii, arr_tmp):
    vrema = sles_rezba(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_frezernaya(ima_operacii, arr_tmp):
    vrema = F.valm(arr_tmp[1][0])
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_sb_pod_sv(ima_operacii, arr_tmp):
    vrema = sb_pod_sv(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_gilotina(ima_operacii, arr_tmp):
    vrema = gilotina(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_otrezka_lentopil(ima_operacii, arr_tmp):
    vrema = otrez_lentopil(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def komp_valcovka(ima_operacii, arr_tmp):
    vrema = valcovka(ima_operacii, arr_tmp)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + "kmp" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    spis = table_kmp(putf)
    for i in range(len(spis)):
        spis[i][-1] = str(round(F.valm(spis[i][-1]) / 450 * vrema, 8))
    return spis


def kontrol_mech_obrabot(ima_operacii, arr_tmp):
    vrem = F.valm(arr_tmp[1][0])*0.1
    return vrem

def kontrol_tcvet_defekt(ima_operacii, arr_tmp):
    dlina_shvov = int(arr_tmp[1][0])/1000
    vremya_tcvet_defect = 34 + dlina_shvov * 5
    return vremya_tcvet_defect

def kontrol_form_i_raspoloj_poverhn(ima_operacii, arr_tmp):
    vid_DSE = str(arr_tmp[1][0])
    razmer = int(arr_tmp[1][1])
    dlina_shvov = int(arr_tmp[1][2])
    koef_DSE = 2
    if vid_DSE == '1':
        koef_DSE = 1
    if vid_DSE == '2':
        koef_DSE = 1.3
    if vid_DSE == '3':
        koef_DSE = 1.5
    vremya_obschee = koef_DSE * (8 * razmer / 1000 + 3 * dlina_shvov / 1000)
    return vremya_obschee

def reykodolbejnaya(ima_operacii, arr_tmp):
    modul = str(arr_tmp[1][0])
    dlina = F.valm(arr_tmp[1][1])/1000
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    N_vr = table(putf, modul) * dlina
    return N_vr


def peremeschenie(ima_operacii, arr_tmp):
    vid = arr_tmp[1][0]
    tr = arr_tmp[1][1]
    ves_det = F.valm(arr_tmp[1][2])
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    if tr == '1':
        koef_kol = 300//ves_det
    else:
        koef_kol = 2100//ves_det
    N_vr = table(putf, vid, tr)/koef_kol
    return N_vr

def komplektov(ima_operacii, arr_tmp):
    massa = F.valm(arr_tmp[1][0])
    if massa <= 0.3:
        Nvr = 2 / 60
    else:
        if massa > 25:
            Nvr = 9/60
        else:
            Nvr = 5/60
    return Nvr

def lazer(ima_operacii, arr_tmp):
    mat = str(arr_tmp[1][0])
    s = F.valm(arr_tmp[1][1])
    obor = str(arr_tmp[1][2])
    kontur = F.valm(arr_tmp[1][3])/ 1000
    vrezi = F.valm(arr_tmp[1][4])
    segmenti = F.valm(arr_tmp[1][5])
    if obor == '0':  # laser
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    else:
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl2.txt'
    skorost = table(putf, mat, s)

    return round((kontur * skorost + vrezi/60)*segmenti, 3)

def lazer_old(ima_operacii, arr_tmp):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';', 'c': 'с', 'C': 'С', 'T': 'Т'}
    for key in slov_zamen.keys():
        arr_tmp[1][5] = arr_tmp[1][5].replace(key, slov_zamen[key])
        arr_tmp[1][6] = arr_tmp[1][6].replace(key, slov_zamen[key])
        arr_tmp[1][7] = arr_tmp[1][7].replace(key, slov_zamen[key])
        arr_tmp[1][8] = arr_tmp[1][8].replace(key, slov_zamen[key])
        arr_tmp[1][9] = arr_tmp[1][9].replace(key, slov_zamen[key])

    no_arr = arr_tmp[1][5].split(";")#число отверстий
    do_arr = arr_tmp[1][6].split(";")#Диаметр отверстий
    np_arr = arr_tmp[1][7].split(";")#Число пазов
    lp_arr = arr_tmp[1][8].split(";")#Длина паза
    bp_arr = arr_tmp[1][9].split(";")#Ширина поаза

    if len(no_arr) != len(do_arr) or len(np_arr) != len(lp_arr) or len(np_arr) != len(bp_arr):
        # CQT.msgbox('Число переменных не корректно')
        return 0

    mat = str(arr_tmp[1][0])
    s = F.valm(arr_tmp[1][1])
    d = F.valm(arr_tmp[1][2])
    l = F.valm(arr_tmp[1][3])
    b = F.valm(arr_tmp[1][4])

    nsec = int(arr_tmp[1][10])
    obor = str(arr_tmp[1][11])

    if obor == '0':  # laser
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    else:
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl2.txt'
    skorost = table(putf, mat, s)

    if d == 0:
        perimetr_konura = (l + b) * 2
        shir = b
    else:
        perimetr_konura = d * 3.141592
        shir = 50
        for i in range(len(no_arr)):
            if F.valm(no_arr[i]) == 1:
                shir = (d- do_arr[i])/2

    perim_otv = 0
    for i in range(len(no_arr)):
        perim_otv = perim_otv + F.valm(no_arr[i]) * F.valm(do_arr[i]) * 3.141592

    perim_paz = 0
    for i in range(len(np_arr)):
        perim_paz = perim_paz + F.valm(np_arr[i]) * (F.valm(lp_arr[i]) + F.valm(bp_arr[i])) * 2

    kontur = ((perimetr_konura + perim_otv + perim_paz) / nsec + (2 * nsec * shir) )/ 1000
    return round(kontur * skorost, 3)


def kantovanie(ima_operacii, arr_tmp):
    massa = int(arr_tmp[1][0])
    ugol = int(arr_tmp[1][1])
    ploskost = int(arr_tmp[1][2])
    tpz = 3
    if ploskost == 0:
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    else:
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table2.txt'
    Nvr = table(putf, ugol, massa)
    N_vr = Nvr
    return N_vr


def sles_razd_krom(ima_operacii, arr_tmp):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';', 'c': 'с', 'C': 'С', 'T': 'Т'}
    for key in slov_zamen.keys():
        arr_tmp[1][0] = arr_tmp[1][0].replace(key, slov_zamen[key])
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])
        arr_tmp[1][2] = arr_tmp[1][2].replace(key, slov_zamen[key])
        arr_tmp[1][3] = arr_tmp[1][3].replace(key, slov_zamen[key])
    material_arr = arr_tmp[1][0].split(";")
    vid_arr = arr_tmp[1][1].split(";")
    dlina_arr = arr_tmp[1][2].split(";")
    tolsh_arr = arr_tmp[1][3].split(";")

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    summ_vr = 0
    for i in range(len(vid_arr)):
        km = 1 if str(material_arr[i]) == '1' else 1.5
        vid = str(vid_arr[i])
        dlina = F.valm(dlina_arr[i])
        tolsh = F.valm(tolsh_arr[i])

        Nvr = table(putf, tolsh, vid)
        N_v = Nvr * dlina * km
        summ_vr += N_v

    return summ_vr


def tokarnaya(ima_operacii, arr_tmp):
    return 0.01


def frezernaya(ima_operacii, arr_tmp):
    return 0.01


def sles_rezba(ima_operacii, arr_tmp):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';'}
    material = str(arr_tmp[1][0])
    for key in slov_zamen.keys():
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])
        arr_tmp[1][2] = arr_tmp[1][2].replace(key, slov_zamen[key])
        arr_tmp[1][3] = arr_tmp[1][3].replace(key, slov_zamen[key])
        arr_tmp[1][4] = arr_tmp[1][4].replace(key, slov_zamen[key])
    n_arr = arr_tmp[1][1].split(";")
    gluh_arr = arr_tmp[1][2].split(";")
    diam_arr = arr_tmp[1][3].split(";")
    glub_arr = arr_tmp[1][4].split(";")

    if len(n_arr) != len(gluh_arr):
        return 0

    summ_vr = 0
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'

    km = 1 if material == '1' else 1.5

    for i in range(len(n_arr)):
        n = F.valm(n_arr[i])
        gluh = str(gluh_arr[i])
        diam = F.valm(diam_arr[i])
        glub = F.valm(glub_arr[i])

        kg = 1.2 if gluh == '1' else 1

        Nvr = table(putf, diam, glub)
        N_v = Nvr * n * km * kg
        summ_vr += N_v

    return summ_vr


def shtamp_perf(ima_operacii, arr_tmp):
    dlina = F.valm(arr_tmp[1][0])
    n = F.valm(arr_tmp[1][1])
    N_vr = dlina / 1000 * 5.6 * n
    return N_vr * 1.2


def sles_sverl(ima_operacii, arr_tmp):
    material = str(arr_tmp[1][0])
    diametr = F.valm(arr_tmp[1][1])
    tolshina = F.valm(arr_tmp[1][2])
    n = F.valm(arr_tmp[1][3])
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    Nvr = table(putf, diametr, tolshina)
    km = 1 if material == '1' else 1.5
    N_vr = Nvr * km * n
    return N_vr


def sverlil(ima_operacii, arr_tmp):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';'}
    material = str(arr_tmp[1][0])
    for key in slov_zamen.keys():
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])
        arr_tmp[1][2] = arr_tmp[1][2].replace(key, slov_zamen[key])
        arr_tmp[1][3] = arr_tmp[1][3].replace(key, slov_zamen[key])
        arr_tmp[1][4] = arr_tmp[1][4].replace(key, slov_zamen[key])
    n_arr = arr_tmp[1][1].split(";")
    gluh_arr = arr_tmp[1][2].split(";")
    diam_arr = arr_tmp[1][3].split(";")
    glub_arr = arr_tmp[1][4].split(";")

    if len(n_arr) != len(gluh_arr):
        return 0

    summ_vr = 0
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'

    km = 1 if material == '1' else 1.5

    for i in range(len(n_arr)):
        n = F.valm(n_arr[i])
        gluh = str(gluh_arr[i])
        diam = F.valm(diam_arr[i])
        glub = F.valm(glub_arr[i])

        kg = 1.1 if gluh == '1' else 1

        Nvr = table(putf, diam, glub)
        N_v = Nvr * n * km * kg
        summ_vr += N_v

    return summ_vr


def sles_prav(ima_operacii, arr_tmp):
    dlina = F.valm(arr_tmp[1][0]) / 1000
    shir = F.valm(arr_tmp[1][1]) / 1000
    tolsh = F.valm(arr_tmp[1][2])
    plosh = dlina * shir

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    Nvr = table(putf, plosh, tolsh)
    return Nvr * 1.2


def drobestrui(ima_operacii, arr_tmp):
    Nvr = 15
    plosh = F.valm(arr_tmp[1][0])
    chislo_mest = F.valm(arr_tmp[1][1])
    slogn_izd = str(arr_tmp[1][2])
    koef = 1.4 if slogn_izd == '1' else 1
    tpz = 1.5
    N_v = Nvr * plosh * koef + tpz * chislo_mest
    return N_v


def otrez_sles(ima_operacii, arr_tmp):
    vid = str(arr_tmp[1][0])
    diametr = F.valm(arr_tmp[1][1])
    tolsh = F.valm(arr_tmp[1][2])
    vis_prof = F.valm(arr_tmp[1][3])
    kol_vo_rez = int(arr_tmp[1][4])
    material = str(arr_tmp[1][5])

    Km = 1.5 if material == '2' else 1
    Nvr = 0
    if vid == '1':
        arr = [1.5, 1.6, 1.7, 1.75, 1.8]
        k_d = 0
        if diametr >= 0 and diametr <= 5:
            k_d = 0
        if diametr > 5 and diametr <= 10:
            k_d = 1
        if diametr > 10 and diametr <= 15:
            k_d = 2
        if diametr > 15 and diametr <= 20:
            k_d = 3
        if diametr > 20 and diametr <= 25000:
            k_d = 4
        Nvr = arr[k_d]
    if vid == '2':
        arr = [1.8, 1.9, 2.05, 2.15, 2.25, 2.3, 2.35, 2.4]
        k_d = 0
        if vis_prof >= 0 and vis_prof <= 20:
            k_d = 1 if tolsh == 4 else 0
        if vis_prof > 20 and vis_prof <= 25:
            k_d = 3 if tolsh == 4 else 2
        if vis_prof > 25 and vis_prof <= 28:
            k_d = 4
        if vis_prof > 28 and vis_prof <= 32:
            k_d = 6 if tolsh == 4 else 5
        if vis_prof > 32 and vis_prof <= 333:
            k_d = 7
        Nvr = arr[k_d]
    if vid == '3':
        arr = [1.5, 1.55, 1.6, 1.65, 1.7]
        k_d = 0
        if diametr >= 0 and diametr <= 8:
            k_d = 0
        if diametr > 8 and diametr <= 10:
            k_d = 1
        if diametr > 10 and diametr <= 12:
            k_d = 2
        if diametr > 12 and diametr <= 14:
            k_d = 3
        if diametr > 14 and diametr <= 25000:
            k_d = 4
        Nvr = arr[k_d]
    if vid == '4':
        arr = [1.9, 2.05, 2.3, 2.75, 3.25, 3.7, 4.2, 4.45, 4.7, 5.2]
        k_d = 0
        if vis_prof >= 0 and vis_prof <= 10:
            k_d = 0
        if vis_prof > 10 and vis_prof <= 15:
            k_d = 1
        if vis_prof > 15 and vis_prof <= 20:
            k_d = 2
        if vis_prof > 20 and vis_prof <= 25:
            k_d = 3
        if vis_prof > 25 and vis_prof <= 30:
            k_d = 4
        if vis_prof > 30 and vis_prof <= 35:
            k_d = 5
        if vis_prof > 35 and vis_prof <= 40:
            k_d = 6
        if vis_prof > 40 and vis_prof <= 42:
            k_d = 7
        if vis_prof > 42 and vis_prof <= 45:
            k_d = 8
        if vis_prof > 45 and vis_prof <= 5000:
            k_d = 9
        Nvr = arr[k_d]
    if vid == '5':
        arr = [0.85, 1.1, 1.65, 2.2, 2.75, 3.3, 3.85, 4.4, 5.5]
        k_d = 0
        if tolsh >= 0 and tolsh <= 1.5:
            k_d = 0
        if tolsh > 1.5 and tolsh <= 2:
            k_d = 1
        if tolsh > 2 and tolsh <= 3:
            k_d = 2
        if tolsh > 3 and tolsh <= 4:
            k_d = 3
        if tolsh > 4 and tolsh <= 5:
            k_d = 4
        if tolsh > 5 and tolsh <= 6:
            k_d = 5
        if tolsh > 6 and tolsh <= 7:
            k_d = 6
        if tolsh > 7 and tolsh <= 8:
            k_d = 7
        if tolsh > 8 and tolsh <= 8888:
            k_d = 8
        Nvr = arr[k_d] / 1000
        Km = kol_vo_rez
    N_v = Nvr * Km
    return N_v


def formovka_linz(ima_operacii, arr_tmp):
    dlina = F.valm(arr_tmp[1][0])
    krug_linz = str(arr_tmp[1][1])
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    Nvr = table(putf, dlina)
    koef = 0.4 if krug_linz == '1' else 1
    N_v = Nvr * dlina / 1000 * koef
    return N_v


def ukladka_nabivki(ima_operacii, arr_tmp):
    plosh = F.valm(arr_tmp[1][0])
    vid_pov = str(arr_tmp[1][1])
    gabarit = F.valm(arr_tmp[1][2])

    if vid_pov == '1':
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
        Nvr = table(putf, gabarit)
    else:
        Nvr = 18

    N_v = Nvr * plosh
    return N_v * 1


def sborka_linz(ima_operacii, arr_tmp):
    material = str(arr_tmp[1][0])
    chislo_uzlov = int(arr_tmp[1][1])
    mass = F.valm(arr_tmp[1][2])
    km = 1.2 if material == '2' else 1
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    Nvr = table(putf, mass, chislo_uzlov)
    N_v = Nvr * km
    return N_v * 1


def svarka(ima_operacii, arr_tmp):
    slov_zamen = {',': '.', ' ': ';', '/': ';', '$': ';', 'c': 'с', 'C': 'С', 'T': 'Т'}
    material = str(arr_tmp[1][0])
    for key in slov_zamen.keys():
        arr_tmp[1][1] = arr_tmp[1][1].replace(key, slov_zamen[key])
        arr_tmp[1][2] = arr_tmp[1][2].replace(key, slov_zamen[key])
        arr_tmp[1][3] = arr_tmp[1][3].replace(key, slov_zamen[key])
        arr_tmp[1][4] = arr_tmp[1][4].replace(key, slov_zamen[key])
    vid_arr = arr_tmp[1][1].split(";")
    dlina_arr = arr_tmp[1][2].split(";")
    tolsh_arr = arr_tmp[1][3].split(";")
    razmetka = arr_tmp[1][4].split(";")

    if len(dlina_arr) != len(vid_arr):
        return 0
    if len(dlina_arr) != len(tolsh_arr):
        return 0

    summ_vr = 0
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table6.txt'
    km = table(putf, material)

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'

    #km = 1 if material == '1' else 1.5
    for i in range(len(vid_arr)):
        dlina = F.valm(dlina_arr[i])
        vid = vid_arr[i]
        tolsh = F.valm(tolsh_arr[i])
        if razmetka[i] == '1':
            kp = 1.5 if dlina > 1500 else 1.9
        else:
            kp = 1
        Nvr = table(putf, tolsh, vid)
        N_v = Nvr * dlina / 1000 * km * kp
        summ_vr += N_v

    return summ_vr


def otrez_lentopil(ima_operacii, arr_tmp):
    material = str(arr_tmp[1][0])
    diametr = F.valm(arr_tmp[1][1])
    vid = str(arr_tmp[1][2])

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    tst = table(putf, diametr, material)
    koef_trub = 0.4 if vid == '2' else 1

    N_v = tst * koef_trub + 1

    return N_v


def okras(ima_operacii, arr_tmp):
    vid_izd = str(arr_tmp[1][0])
    tip_oborud = str(arr_tmp[1][1])
    dlina = F.valm(arr_tmp[1][2])
    shirina = F.valm(arr_tmp[1][3])
    slognost = str(arr_tmp[1][4])
    ploshad = F.valm(arr_tmp[1][5])
    ch_st_shp = int(arr_tmp[1][6])

    gabarit = dlina if dlina > shirina else shirina

    if tip_oborud == '1':
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    else:
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl2.txt'

    nvr = table(putf, gabarit, slognost)

    if vid_izd == '1':
        N_v = ploshad * nvr + ch_st_shp * 6.5
    elif vid_izd == '2':
        N_v = ploshad * nvr + ch_st_shp * 0.4
    else:
        N_v = ploshad * nvr

    return N_v


def gilotina(ima_operacii, arr_tmp):
    rezi = int(arr_tmp[1][0])
    rezi = 4 if rezi > 4 else rezi
    if rezi == 1:
        N_v = 3.3
    elif rezi == 2:
        N_v = 4.6
    elif rezi == 3:
        N_v = 5.3
    elif rezi == 4:
        N_v = 6
    return N_v


def sles_zausenci(ima_operacii, arr_tmp):
    material = int(arr_tmp[1][0])
    partia = int(arr_tmp[1][1])
    plosh = F.valm(arr_tmp[1][2])
    perimetr = F.valm(arr_tmp[1][3]) / 1000

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    koef = table(putf, partia)

    if material == 1:
        N_v = 12.65 * plosh * koef
    else:
        N_v = 0.64 * perimetr * koef

    return N_v


def gravir(ima_operacii, arr_tmp):
    dlina = F.valm(arr_tmp[1][0])
    shir = F.valm(arr_tmp[1][1])
    shirm = shir / 1000
    dlinam = dlina / 1000
    plosh = dlinam * shirm
    N_v = 0.17 + 113 * plosh
    return N_v


def sb_pod_sv(ima_operacii, arr_tmp):
    mass = F.valm(arr_tmp[1][0])
    kol_vo = int(arr_tmp[1][1])
    vid = str(arr_tmp[1][2])
    material = int(arr_tmp[1][3])

    km = 1 if material == 1 else 1.2
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    if vid == '2':
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table2.txt'
    if vid == '3':
        putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table3.txt'
    nvr = table(putf, mass, kol_vo)

    N_v = nvr * km
    return N_v * 1


def sles_zach_shvov(ima_operacii, arr_tmp):
    tip = str(arr_tmp[1][0])
    gabarit = F.valm(arr_tmp[1][1])
    d_shvov = F.valm(arr_tmp[1][2])
    material = int(arr_tmp[1][3])
    tolsh = F.valm(arr_tmp[1][4])

    km = 1 if material == 1 else 1.85

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table2.txt'
    kt = table(putf, tolsh)

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'table1.txt'
    nvr = table(putf, tip, gabarit)
    N_v = nvr * d_shvov / 1000 * km * kt
    return N_v


def sbor_obsh(ima_operacii, arr_tmp):
    material = int(arr_tmp[1][0])
    chislo_det = int(arr_tmp[1][1])
    massa = F.valm(arr_tmp[1][2])

    koef = 1 if material == 1 else 1.2
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    nvr = table(putf, massa, chislo_det)
    N_v = nvr * koef
    return N_v * 1


def gibka(ima_operacii, arr_tmp):
    material = int(arr_tmp[1][0])
    chislo_gibov = int(arr_tmp[1][1])
    dlina_det = F.valm(arr_tmp[1][2])
    shirina = F.valm(arr_tmp[1][3])
    chislo_partii = int(arr_tmp[1][4])
    massa = F.valm(arr_tmp[1][5])

    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    nvr = table(putf, chislo_gibov, dlina_det)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl2.txt'
    kp = table(putf, chislo_partii)
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl3.txt'
    km = table(putf, massa)
    koef = 0
    if material != 1:
        summ = (dlina_det + shirina) * 2
        koef = summ / 1000 * 0.64
    N_v = (nvr + koef) * kp * km
    return N_v


def valcovka(ima_operacii, arr_tmp):
    tolsch = F.valm(arr_tmp[1][0])
    diametr = F.valm(arr_tmp[1][1])
    putp = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + ima_operacii + '.txt'
    N_v = table(putp, tolsch, diametr)
    return N_v * 1

def valtcovka_linz(ima_operacii, arr_tmp): 
    diametr_linz = int(arr_tmp[1][0])
    putf = F.scfg('cash') + F.sep() + "tables" + F.sep() + ima_operacii + F.sep() + 'tabl1.txt'
    Nvr = table(putf, diametr_linz)
    return Nvr

def table(putf, vert, gor=None, rez_valm=True):
    if F.nalich_file(putf) == False:
        return 0
    spis = F.otkr_f(putf, separ='|', utf8=True)
    row = False
    if type(vert) == type(2) or type(vert) == type(2.2):
        for i in range(1, len(spis)):
            if vert <= F.valm(spis[i][0]):
                row = i
                break
    else:
        for i in range(1, len(spis)):
            if vert.upper() == spis[i][0].upper():
                row = i
                break
    if row == False:
        return 0
    if gor == None:
        if rez_valm:
            return F.valm(spis[row][1])
        else:
            return spis[row][1]
    kol = False
    if type(gor) == type(2) or type(gor) == type(2.2):
        for i in range(1, len(spis[0])):
            if gor <= int(spis[0][i]):
                kol = i
                break
    else:
        for i in range(1, len(spis[0])):
            if gor.upper() == spis[0][i].upper():
                kol = i
                break
    if kol == False:
        return 0
    if rez_valm:
        return F.valm(spis[row][kol])
    else:
        return spis[row][kol]


def table_kmp(putf):
    if F.nalich_file(putf) == False:
        return []
    spis = F.otkr_f(putf, separ='|', utf8=True)
    return spis
