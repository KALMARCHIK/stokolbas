import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from products.models import Product, Category
import requests
import os
from django.conf import settings
from time import sleep
import slugify
from urllib.parse import urlparse
from rapidfuzz import fuzz, process

options = uc.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

def save_image(products=None):
    parser_names = {'КОЛБАСЫ ВАРЕНЫЕ': [{'ДОКТОРСКАЯ ЛЮКС': ['https://www.kmk.by/catalog/kolbasy-varenye/doktorskaja-ljuks/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__doktorskaja-ljuks-srez-b-s.webp']}, {'МОЛОЧНАЯ НЕЖНАЯ': ['https://www.kmk.by/catalog/kolbasy-varenye/molochnaja-nezhnaja/', 'https://www.kmk.by/wp-content/uploads/2024/05/molochnaja.webp']}, {'ЭСТОНСКАЯ ЛАКОМАЯ': ['https://www.kmk.by/catalog/kolbasy-varenye/jestonskaja-lakomaja/', 'https://www.kmk.by/wp-content/uploads/2024/05/jestonskaja.webp']}, {'СЛИВОЧНАЯ': ['https://www.kmk.by/catalog/kolbasy-varenye/slivochnaja/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__slivochnaja-srez-b-s-2.webp']}, {'КАК РАНЬШЕ': ['https://www.kmk.by/catalog/kolbasy-varenye/kak-ranshe/', 'https://www.kmk.by/wp-content/uploads/2024/05/kak-ranshe.webp']}, {'МОРТАДЕЛЛА ЛЮКС': ['https://www.kmk.by/catalog/kolbasy-varenye/mortadella-ljuks/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__mortadella-srez-b-s.webp']}, {'ДОКТОРСКАЯ ЭЛИТ': ['https://www.kmk.by/catalog/kolbasy-varenye/doktorskaja-jelit/', 'https://www.kmk.by/wp-content/uploads/2024/05/doktorskaja-jelit.webp']}, {'ЭСТОНСКАЯ ЛАКОМАЯ': ['https://www.kmk.by/catalog/kolbasy-varenye/jestonskaja-lakomaja-v-naturalnoj-obolochke/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__jestonskaja-lakomaja-v-s-srez-s-s-mb.webp']}, {'ДОКТОРСКАЯ С МАСЛИЦЕМ': ['https://www.kmk.by/catalog/kolbasy-varenye/doktorskaja-s-maslicem/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__frame-2-mb.webp']}, {'МОЛОЧНАЯ ЛАКОМАЯ': ['https://www.kmk.by/catalog/kolbasy-varenye/molochnaja-lakomaja/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__molochnaja-lakomaja-380-gr-1-2-mb.webp']}, {'ОБЫЧНАЯ': ['https://www.kmk.by/catalog/kolbasy-varenye/obychnaja/', 'https://www.kmk.by/wp-content/uploads/2024/05/obychnaja.webp']}, {'ВКУСНАЯ НОВАЯ': ['https://www.kmk.by/catalog/kolbasy-varenye/vkusnaja-novaja-vysshego-sorta/', 'https://www.kmk.by/wp-content/uploads/2024/05/vkusnaja.webp']}, {'БОЯРУШКА': ['https://www.kmk.by/catalog/kolbasy-varenye/bojarushka/', 'https://www.kmk.by/wp-content/uploads/2024/05/bojarushka.webp']}, {'СУДАРУШКА': ['https://www.kmk.by/catalog/kolbasy-varenye/sudarushka/', 'https://www.kmk.by/wp-content/uploads/2024/05/sudarushka.webp']}], 'СОСИСКИ И САРДЕЛЬКИ': [{'СОСИСКИ ДОКТОРСКИЕ ПРЕСТИЖ': ['https://www.kmk.by/catalog/sosiski-i-sardelki/sosiski-doktorskie-prestizh/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__sosiski-doktorskie-razrez-mb.webp']}, {'СОСИСКИ СЛИВОЧНЫЕ ЛЮКС': ['https://www.kmk.by/catalog/sosiski-i-sardelki/sosiski-krakovskie-novye/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__sosiski-slivochnye-razrez-mb.webp']}, {'СОСИСКИ КРАКОВСКИЕ НОВЫЕ': ['https://www.kmk.by/product/534/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__sosiski-krakovskie-razrez-mb.webp']}, {'СОСИСКИ МОЛОЧНЫЕ ЛАКОМЫЕ': ['https://www.kmk.by/catalog/sosiski-i-sardelki/sosiski-molochnye-lakomye/', 'https://www.kmk.by/wp-content/uploads/2024/05/molochnye-m.webp']}, {'СОСИСКИ МИНУТКИ': ['https://www.kmk.by/catalog/sosiski-i-sardelki/sosiski-minutki/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__minutki-1.webp']}, {'СОСИСКИ ВКУСНЫЕ С СЫРОМ ЭЛИТ': ['https://www.kmk.by/catalog/sosiski-i-sardelki/sosiski-vkusnye-s-syrom-jelit/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__sosiski-sosiski-razrez-mb.webp']}, {'САРДЕЛЬКИ ТОЛСТЯЧКИ С СЫРОМ': ['https://www.kmk.by/product/547/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__sardelki-tolstjachki-mb.webp']}, {'САРДЕЛЬКИ МОРТАДЕЛКИ ЛЮКС': ['https://www.kmk.by/catalog/sosiski-i-sardelki/sardelki-mortadelki-ljuks/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__sardelki-mortadelki-mb.webp']}, {'САРДЕЛЬКИ ТЕЛЯЧЬИ': ['https://www.kmk.by/catalog/sosiski-i-sardelki/sardelki-teljachi/', 'https://www.kmk.by/wp-content/uploads/2024/05/anyconv.com__sardelki-mortadelki-mb.webp']}], 'КОЛБАСЫ ПОЛУКОПЧЕНЫЕ': [], 'ВАРЕНО-КОПЧЕНЫЕ КОЛБАСЫ': [{'КРЕМЛЕВСКАЯ ОСОБАЯ САЛЯМИ': ['https://www.kmk.by/catalog/vareno-kopchenye-kolbasy/kremlevskaja-osobaja-saljami-2/', 'https://www.kmk.by/wp-content/uploads/2024/07/kremlevskaja-osobaja-mg.webp']}, {'ПОСОЛЬСКАЯ': ['https://www.kmk.by/catalog/vareno-kopchenye-kolbasy/posolskaja/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__posolskaja-v_k-mb.webp']}, {'СЕРВЕЛАТ ОРЕХОВЫЙ': ['https://www.kmk.by/catalog/vareno-kopchenye-kolbasy/servelat-orehovyj/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__orehovyj-servelat-mb.webp']}, {'ПАРМСКАЯ ЭЛИТ': ['https://www.kmk.by/product/1068/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__parmskaja-jelit-1.webp']}, {'ФИНСКИЙ СЕРВЕЛАТ': ['https://www.kmk.by/catalog/finskij-servelat/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__finskij-servelat-fiksirovannyj-ves-po-380-gr-mb.webp']}, {'МОМБИЛЬЕР': ['https://www.kmk.by/catalog/vareno-kopchenye-kolbasy/mombiler/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__mb-1-2.webp']}, {'ПОЛЕССКАЯ': ['https://www.kmk.by/catalog/vareno-kopchenye-kolbasy/polesskaja/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__polesskaja-mb.webp']}, {'МИНСКАЯ ЛЮКС': ['https://www.kmk.by/catalog/vareno-kopchenye-kolbasy/minskaja-ljuks/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__minskaja-m.webp']}], 'КОЛБАСЫ СЫРОКОПЧЕНЫЕ И СЫРОВЯЛЕНЫЕ': [{'КРЕМЛЕВСКАЯ ПРЕСТИЖ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/kremlevskaya-prestizh/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__kremlevskaja-s_k-1-mb.webp']}, {'САЛЬЧИЧОН': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/salchichon/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__salchichon-mb.webp']}, {'ПЕППЕРОНИ ПРЕМИУМ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/pepperoni-premium/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__pepperoni-mb.webp']}, {'ОРИГИНАЛЬНАЯ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/originalnaja/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__originalnaja-mb.webp']}, {'ИТАЛЬЯНСКАЯ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/italjanskaja/', 'https://www.kmk.by/wp-content/uploads/2024/05/italjanskaja-m.webp']}, {'ЗАКУСКА ИЗ ДЕРЕВНИ СВИНАЯ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/zakuska-iz-derevni-svinaja/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__zakuska-iz-derevni-svinaja-mb.webp']}, {'ЗАКУСКА ДЕДОВСКАЯ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/zakuska-dedovskaja/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__zakuska-dedovskaja-mb.webp']}, {'ВЕНЕЦИАНСКАЯ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/venecianskaja/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__venecianskaja-pc-2.webp']}, {'МАДЬЯРСКАЯ': ['https://www.kmk.by/catalog/kolbasy-syrokopchenye-i-syrovjalenye/madjarskaja/', 'https://www.kmk.by/wp-content/uploads/2024/10/anyconv.com__madjarskaja-mb.webp']}], 'ПРОДУКТЫ ИЗ МЯСА СВИНИНЫ': [{'ПРОДУКТ ИЗ СВИНИНЫ КОПЧЕНО-ВАРЕНЫЙ «КАРБОНАТ КНЯЖЕСКИЙ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/produkt-iz-svininy-kopcheno-varenyj-karbonat-knjazheskij/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__karbonat-knjazheskij-mb.webp']}, {'ПРОДУКТ ИЗ СВИНИНЫ КОПЧЕНО-ВАРЕНЫЙ «ЛОПАТКА ЦАРСКАЯ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/produkt-iz-svininy-kopcheno-varenyj-lopatka-carskaja/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__lopatka-carskaja-mb.webp']}, {'ПРОДУКТ ИЗ СВИНИНЫ КОПЧЕНО-ВАРЕНЫЙ «ПОЛОСКА КНЯЖЕСКАЯ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/produkt-iz-svininy-kopcheno-varenyj-poloska-knjazheskaja/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__poloska-knjazheskaja-mb.webp']}, {'ПРОДУКТ ИЗ СВИНИНЫ КОПЧЕНО-ВАРЕНЫЙ «БУЖЕНИНА ЦАРСКАЯ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/produkt-iz-svininy-kopcheno-varenyj-buzhenina-carskaja/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__buzhenina-carskaja.webp']}, {'ПРОДУКТ ИЗ СВИНИНЫ КОПЧЕНО-ВАРЕНЫЙ «КОВАЛОЧЕК КНЯЖЕСКИЙ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/produkt-iz-svininy-kopcheno-varenyj-kovalochek-knjazheskij/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__kovalochek-knjazheskij-mb.webp']}, {'ПРОДУКТ ИЗ СВИНИНЫ СЫРОКОПЧЕНЫЙ «КУМПЯЧОК»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/produkt-iz-svininy-kopcheno-varenyj-kumpjachok/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__kumpjachok-mb.webp']}, {'ПРОДУКТ ИЗ СВИНИНЫ СЫРОКОПЧЕНЫЙ «ВЫРЕЗКА ДОМАШНЯЯ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/produkt-iz-svininy-kopcheno-varenyj-vyrezka-domashnjaja/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__domashnjaja-vyrezka-mb.webp']}, {'ПРОДУКТ ИЗ СВИНИНЫ СЫРОКОПЧЕНЫЙ «ГОСТИНЕЦ ПАНСКИЙ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/gostinec-panskij/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__gostinec-panskij-mb-2.webp']}, {'ЧИПСЫ МЯСНЫЕ ВЕНСКИЕ': ['https://www.kmk.by/catalog/produkty-iz-mjasa-svininy/chipsy-mjasnye-venskie/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__frame-1000002990.webp']}], 'ПРОДУКТЫ ИЗ МЯСА ГОВЯДИНЫ': [{'ПРОДУКТ КОПЧЕНО-ВАРЕНЫЙ БОЧОНОК «ФИРМЕННЫЙ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-govjadiny/produkt-kopcheno-varenyj-bochonok-firmennyj/', 'https://www.kmk.by/wp-content/uploads/2025/01/bochonok-firmennyj-k-v-mb.webp']}, {'ПРОДУКТ КОПЧЕНО-ВАРЕНЫЙ ГОВЯДИНА «ПРАЗДНИЧНАЯ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-govjadiny/produkt-kopcheno-varenyj-govjadina-prazdnichnaja/', 'https://www.kmk.by/wp-content/uploads/2025/01/3.webp']}, {'ПРОДУКТ КОПЧЕНО-ВАРЕНЫЙ ЗАКУСКА «КНЯЖЕСКАЯ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-govjadiny/produkt-kopcheno-varenyj-zakuska-knjazheskaja/', 'https://www.kmk.by/wp-content/uploads/2025/01/5-2.webp']}, {'ПРОДУКТ СЫРОКОПЧЕНЫЙ ГОВЯЖИЙ ВЫРЕЗКА «БАРСКАЯ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-govjadiny/produkt-syrokopchenyj-govjazhij-vyrezka-barskaja/', 'https://www.kmk.by/wp-content/uploads/2025/01/3-2.webp']}, {'ПРОДУКТ ИЗ ГОВЯДИНЫ СЫРОКОПЧЕНЫЙ «САНТОРИНИ»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-govjadiny/produkt-iz-govjadiny-syrokopchenyj-santorini/', 'https://www.kmk.by/wp-content/uploads/2025/01/2-1.webp']}, {'ПРОДУКТ СЫРОКОПЧЕНЫЙ ИЗ ГОВЯДИНЫ «ТОСКАНО»': ['https://www.kmk.by/catalog/produkty-iz-mjasa-govjadiny/produkt-syrokopchenyj-iz-govjadiny-toskano/', 'https://www.kmk.by/wp-content/uploads/2025/01/toskano-mb.webp']}, {'ЧИПСЫ МЯСНЫЕ ОРИГИНАЛЬНЫЕ': ['https://www.kmk.by/catalog/produkty-iz-mjasa-govjadiny/chipsy-myasnye/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__frame-20461.webp']}], 'ПРОДУКТЫ ИЗ МЯСА ПТИЦЫ': [], 'КОЛБАСНЫЕ ИЗДЕЛИЯ И ПРОДУКТЫ ИЗ СУБПРОДУКТОВ': [], 'КОНСЕРВЫ': [{'КОНСЕРВЫ «СВИНИНА ТУШЕНАЯ» ГОСТ 32125-2013': ['https://www.kmk.by/catalog/konservy/konservy-svinina-tushenaja-gost-32125-2013/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__svinina-tushenaja-gost2-mb.webp']}, {'КОНСЕРВЫ «ГОВЯДИНА ТУШЕНАЯ» ГОСТ 32125-2013': ['https://www.kmk.by/catalog/konservy/konservy-govjadina-tushenaja-gost-32125-2013/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__govjadina-gost-mb.webp']}, {'КОНСЕРВЫ «ГОВЯДИНА ТУШЕНАЯ ПРЯНАЯ»': ['https://www.kmk.by/catalog/konservy/konservy-govjadina-tushenaja-prjanaja/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__konservy-mokap-b.webp']}, {'КОНСЕРВЫ МЯСОРАСТИТЕЛЬНЫЕ «КАША ПЕРЛОВАЯ СО СВИНИНОЙ» ГОСТ 8286-90': ['https://www.kmk.by/catalog/konservy/konservy-mjasorastitelnye-kasha-perlovaja-so-svininoj-gost-8286-90/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__kasha-perlovaja-so-svininoj-mb.webp']}, {'КОНСЕРВЫ МЯСОРАСТИТЕЛЬНЫЕ «КАША ПЕРЛОВАЯ С ГОВЯДИНОЙ» ГОСТ 8286-90': ['https://www.kmk.by/product/1156/', 'https://www.kmk.by/wp-content/uploads/2024/08/kasha-perlovaja-s-govjadinoj-1-mb.png']}, {'КОНСЕРВЫ МЯСОРАСТИТЕЛЬНЫЕ «КАША РИСОВАЯ С ГОВЯДИНОЙ» ГОСТ 8286-90': ['https://www.kmk.by/catalog/konservy/konservy-mjasorastitelnye-kasha-risovaja-s-govjadinoj-gost-8286-90/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__kasha-risovaja-s-govjadinoj-1.webp']}, {'КОНСЕРВЫ МЯСОРАСТИТЕЛЬНЫЕ «КАША ГРЕЧНЕВАЯ С ГОВЯДИНОЙ» ГОСТ 8286-90': ['https://www.kmk.by/catalog/konservy/konservy-mjasorastitelnye-kasha-grechnevaja-s-govjadinoj-gost-8286-90/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__kasha-grechnevaja-s-govjadinoj-mb.webp']}, {'КОНСЕРВЫ МЯСОРАСТИТЕЛЬНЫЕ «КАША РИСОВАЯ СО СВИНИНОЙ» ГОСТ 8286-90': ['https://www.kmk.by/catalog/konservy/konservy-mjasorastitelnye-kasha-risovaja-so-svininoj-gost-8286-90/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__kasha-risovaja-so-svininoj-mb.webp']}, {'КОНСЕРВЫ ДЛЯ СОБАК И КОШЕК АППЕТИТНЫЕ ТУ BY 400023328.011-2018': ['https://www.kmk.by/product/1165/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__konservy-dlja-sobak-i-koshek-mb.webp']}], 'ПЕЛЬМЕНИ': [{'ПЕЛЬМЕНИ «ЛЮБИМЫЕ С МОЛОКОМ»': ['https://www.kmk.by/catalog/pelmeni/pelmeni-ljubimye-s-molokom/', 'https://www.kmk.by/wp-content/uploads/2024/08/frame_1000003245.webp']}, {'ПЕЛЬМЕНИ «ЦАРСКИЕ»': ['https://www.kmk.by/catalog/pelmeni/pelmeni-carskie/', 'https://www.kmk.by/wp-content/uploads/2024/08/frame_1000003247.webp']}, {'ПЕЛЬМЕНИ «ОБЖОРКИ ЛЮБИМЫЕ»': ['https://www.kmk.by/catalog/pelmeni/pelmeni-obzhorki-ljubimye/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__pelmeni-obzhorki-mb-scaled.webp']}, {'ПЕЛЬМЕНИ «ПО-ДОМАШНЕМУ»': ['https://www.kmk.by/catalog/pelmeni/pelmeni-po-domashnemu/', 'https://www.kmk.by/wp-content/uploads/2024/08/frame_1000003249.webp']}, {'ПЕЛЬМЕНИ «БАБУШКИНЫ»': ['https://www.kmk.by/catalog/pelmeni/pelmeni-babushkiny/', 'https://www.kmk.by/wp-content/uploads/2024/08/frame_1000003251.webp']}, {'ПЕЛЬМЕНИ «КУПЕЧЕСКИЕ»': ['https://www.kmk.by/catalog/pelmeni/pelmeni-kupecheskie/', 'https://www.kmk.by/wp-content/uploads/2024/12/frame_1000003255.webp']}], 'ПОЛУФАБРИКАТЫ': [{'ЛОПАТКА ДЛЯ ЗАПЕКАНИЯ': ['https://www.kmk.by/catalog/polufabrikaty/lopatka-dlja-zapekanija/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__4-pc.webp']}, {'БЕДРО В МАРИНАДЕ': ['https://www.kmk.by/catalog/polufabrikaty/bedro-v-marinade/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__1-mb.webp']}, {'ГОЛЕНЬ В МАРИНАДЕ': ['https://www.kmk.by/catalog/polufabrikaty/golen-v-marinade/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__2-mb.webp']}, {'СВИНИНА ДОМАШНЯЯ В МАРИНАДЕ': ['https://www.kmk.by/catalog/polufabrikaty/svinina-domashnjaja-v-marinade/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__3-mb.webp']}, {'ШКВАРКА ФИРМЕННАЯ': ['https://www.kmk.by/catalog/polufabrikaty/shkvarka-firmennaja/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__7-mb.webp']}, {'ШЕЯ НЕЖНАЯ': ['https://www.kmk.by/catalog/polufabrikaty/sheja-nezhnaja/', 'https://www.kmk.by/wp-content/uploads/2024/12/anyconv.com__5-mb.webp']}, {'ПОЛЕНДВИЦА ДЛЯ ЗАПЕКАНИЯ': ['https://www.kmk.by/catalog/polufabrikaty/polendvica-dlja-zapekanija/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__polendvica-mb.webp']}, {'ЛОПАТКА': ['https://www.kmk.by/catalog/polufabrikaty/lopatka/', 'https://www.kmk.by/wp-content/uploads/2024/07/anyconv.com__lopatka-mb.webp']}, {'СВИНИНА ДОМАШНЯЯ ДЛЯ ЗАПЕКАНИЯ': ['https://www.kmk.by/catalog/polufabrikaty/svinina-domashnjaja-dlja-zapekanija/', 'https://www.kmk.by/wp-content/uploads/2024/08/anyconv.com__svinina-domashnjaja-mb.webp']}]}
    spliters = [
        '2/с',
        '1/с',
        'к/в',
        'с/к',
        'в/к',
        'с/в',
        '/в',
        'в/с',
        '/',
        '   ',
        '  ',
        'н/о',
        'газ',
        '(газ)',
        'вар',
        'вар.',
        'руб.', 
        'иск.',
        'руб',
        'в/у',
        '(в/у)',
        '/таз. часть/',
        '/таз.',
        '/шейн. часть/',
        '(текс. об.)',


    ]
    db = list(Product.objects.all())
    db_clean_name = {}
    for i in db:
        try: 
            db_clean_name[str(i.category)]
        except:
            db_clean_name[str(i.category)] = []
        name = [i.replace(' ', '') for i in str(i.name).split(' ')]
        short_name = [i.replace(' ', '') for i in ' '.join(name[0:3]).split(' ')]
        for a in short_name:
            if a in spliters:
                short_name.remove(a)
        db_clean_name[str(i.category)].append(' '.join(short_name))
    
    cat_parser = [k.lower() for k, v in parser_names.items()]
    cat_db = [k.lower() for k, v in db_clean_name.items()]
    
    matching_dict = {}

    # Проходим по первому массиву
    for item1 in cat_db:
        # Используем fuzzywuzzy для поиска наиболее похожего совпадения
        match = process.extractOne(item1, cat_parser, scorer=fuzz.WRatio)
        
        if match and match[1] > 55:  # Порог схожести (чем выше, тем точнее совпадение)
            # Если совпадение найдено, добавляем в словарь
            matching_dict[item1] = match[0]
            cat_db.remove(item1)  # Удаляем найденную строку из первого массива
            cat_parser.remove(match[0])  # Удаляем найденную строку из второго массива
        else:
            print(f'Не найдено подходящего совпадения для: {item1}')
    for item1 in cat_db:
        # Используем fuzzywuzzy для поиска наиболее похожего совпадения
        match = process.extractOne(item1, cat_parser, scorer=fuzz.WRatio)
        
        if match and match[1] > 55:  # Порог схожести (чем выше, тем точнее совпадение)
            # Если совпадение найдено, добавляем в словарь
            matching_dict[item1] = match[0]
            cat_db.remove(item1)  # Удаляем найденную строку из первого массива
            cat_parser.remove(match[0])  # Удаляем найденную строку из второго массива
        else:
            print(f'Не найдено подходящего совпадения для: {item1}')
    # Выводим результат
    print('Сопоставления:')
    print(matching_dict)

    # Выводим оставшиеся строки, для которых не нашли совпадений
    if cat_db:
        print('Не найдено совпадений для этих строк из первого массива:')
        print(cat_db)

    if cat_parser:
        print('Не найдено совпадений для этих строк из второго массива:')
        print(cat_parser)
    
        

    # print(db_clean_name)
def kalinko_parser(supplier=None):
    category_list = {}

    driver.get('https://www.kmk.by/catalog/')
    sleep(1)
    cards = driver.find_elements(By.XPATH, "/html/body/div[2]/main/div/section/div/div/div/div")
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    for card in cards:
        # Извлекаем ссылку и название категории из <a>
        
        link_element = card.find_element(By.CSS_SELECTOR, "h3.category-card__title a")
        category_name = link_element.text
        category_link = link_element.get_attribute("href")

        # Извлекаем изображение
        sleep(0.5)
        try:
            img_element = card.find_element(By.CSS_SELECTOR, "img.category-card__image")
            img_src = img_element.get_attribute("src")
            category_list[category_name] = [category_link, img_src] 
        except Exception as e:
            print(e)
    
    res = {}
    for key, value in category_list.items():
        
        driver.get(value[0])
        sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1.5)
        cards = driver.find_elements(By.CLASS_NAME, 'product-card')
        sleep(1)
        prom_res = []
        for card in cards:
            sleep(1)
            image_element = card.find_element(By.CLASS_NAME, 'product-card__image-media')
            sleep(0.5)
            image_src = image_element.get_attribute("src")

            product_element = card.find_element(By.CLASS_NAME, 'product-card__link')
            product_name = product_element.text
            product_link = product_element.get_attribute("href")
            prom_res.append({product_name: [product_link, image_src]})
    
        res[key] = prom_res
    print(res)
    driver.close()

