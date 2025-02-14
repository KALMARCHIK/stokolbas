from products.models import Category, Product
import requests
from bs4 import BeautifulSoup
from parsers.excel_parser import extract_prices
# from g4f.client import Client
from fuzzywuzzy import fuzz
# options = uc.ChromeOptions()
# # options.add_argument()  
# options.add_argument("--disable-blink-features=AutomationControlled")
# driver = uc.Chrome(options=options)

def ask_gpt(content):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{content}"}],
        web_search=False
    )
    return response.choices[0].message.content


def start_parsing(suppliers):
    for i in suppliers:
        if i.name == 'Калинковичский мясокомбинат':
            parser_kalinko(i)
        elif i.name == 'Березовский мясокомбинат':
            parser_bereza(i)


def parser_kalinko(kalinko):    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
    data_cat = requests.get(kalinko.website, headers=header)
    bs_cat = BeautifulSoup(data_cat.text, 'html.parser')
    
    ######################
    # Загрузка категорий #
    ######################
    category = {}
    category_divs = bs_cat.find_all('div', class_='category-card')
    for i in category_divs:
        tag_a = i.find('a', class_='category-card__link')
        name = tag_a.text
        while "  " in name:
            name = name.replace("  ", " ")
        category[name] = {'href': tag_a.get('href'), 'img': i.find('img', class_='category-card__image').get('data-src')}
    unique_categories = set([k for k, v in category.items()])  # Только уникальные значения
    existing_categories = set(Category.objects.filter(supplier=kalinko).values_list('name', flat=True))
    # new_categories = [Category(name=cat, supplier=kalinko, image=category[cat]['img']) for cat in unique_categories if cat not in existing_categories]
    for cat in unique_categories:
        if cat not in existing_categories:
            try:
                new_category = Category.objects.create(name=cat, image=category[cat]['img'], supplier=kalinko)
                # new_categories.append(new_category)
            except Exception as e:
                print(e)

    ####################
    # Загрузка товаров #
    ####################
    # Загрузка данных товаров 
    products = {}
    for k, v in category.items():
        data_prod = requests.get(v['href'], headers=header)
        bs_prod = BeautifulSoup(data_prod.text, 'html.parser')
        products[k] = {}
        
        for card in bs_prod.find_all('div', class_='product-card'):
            product_a = card.find('a', class_='product-card__link')
            valid = card.find('p', class_='product-card__category')
            img = card.find('img', class_='product-card__image-media').get('data-src')
            name = product_a.text
            while "  " in name:
                name.replace("  ", " ")
                while '\n' in name:
                    name = name.replace("\n", "")
                
                
            print(name)
            products[k][name[1:-1]] = {
                'href': product_a.get('href'), 
                'img': img,
                'valid': valid.text, 
                }


    for k, v in products.items():
        for a, i in v.items():
            data__prod = requests.get(i['href'], headers=header)
            bs__prod = BeautifulSoup(data__prod.text, 'html.parser')
            product_card = bs__prod.find('div', class_='product-single')
            
            try:
                products[k][a]['implementation_period'] = [i.text for i in product_card.select('ul > li:nth-child(4) > div')]
            except Exception as e:
                print(e)
                products[k][a]['implementation_period'] = []
                print(f'Срок реализации для товара {a} не найден')
    
    __prod = [list(v.keys()) for k, v in products.items()]
    unique_products = []
    for a in __prod:
        for i in a:
            unique_products.append(i.replace('\n', '')[1:-1])
    
    existing_products = set(Product.objects.filter(supplier=kalinko).values_list('name', flat=True))
    prices = extract_prices(kalinko.price_list)
    prices_keys = list(extract_prices(kalinko.price_list).keys())
    
    # Порог схожести (от 0 до 100)
    threshold = 80

    # Поиск совпадений
    matches = {}
    for item_A in unique_products:
        best_match = None
        best_score = 0
        for item_B in prices_keys:
            score = fuzz.token_set_ratio(item_A.lower(), item_B.lower())  # Оценка схожести
            if score > best_score:
                best_score = score
                best_match = item_B
        if best_score >= threshold:
            matches[item_A] = best_match
        else:
            matches[item_A] = 'Не найдено'

    # Вывод результатов
    # for key, value in matches.items():
    #     print(f"'{key}': '{value}'")
    # print(existing_products)

    # _category = 
    for b in category:
        # print(b)
        # print('+++++++++++++++')
        for k, v in products[b].items():
            # print(k)
            # print(v)
            print('----------------')
            if matches[k] != 'Не найдено':
                print(matches[k])
                try:
                    Product.objects.create(name=k, category=Category.objects.filter(name=b), price=prices[v][0], valid=products[b][k]['valid'], implementation_period=products[b][k]['implementation_period'], bulk_price=prices[v][1], image=products[b][k]['img'], supplier=kalinko)
                    
                except Exception as e:
                    print(e)



    # prod_with_price = ask_gpt(f'Привет найди каждому элементу из этого списка {unique_products}, максимально подходящий элемент из этого списка {prices_keys}. Элементы из второго списка не должны использоваться два раза, если не можешь найти максимально подходящий элемент то ставь занчение не найдено. Сформируй словарь где ключ это значение из первого списка, а значение словаря это найденное значение из второго списка. Верни в ответе просто словарь без названия')[10::]
    # # parse_dict = json.loads(prod_with_price)
    # print(prod_with_price)
def parser_bereza(bereza):pass