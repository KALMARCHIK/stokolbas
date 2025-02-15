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
        name = tag_a.text.strip()
        category[name] = {'href': tag_a.get('href'), 'img': i.find('img', class_='category-card__image').get('data-src')}
    
    existing_categories = set(Category.objects.filter(supplier=kalinko).values_list('name', flat=True))
    for cat, data in category.items():
        if cat not in existing_categories:
            try:
                Category.objects.create(name=cat, image=data['img'], supplier=kalinko)
            except Exception as e:
                print(e)
    
    ####################
    # Загрузка товаров #
    ####################
    products = {}
    for k, v in category.items():
        data_prod = requests.get(v['href'], headers=header)
        bs_prod = BeautifulSoup(data_prod.text, 'html.parser')
        products[k] = {}
        
        for card in bs_prod.find_all('div', class_='product-card'):
            product_a = card.find('a', class_='product-card__link')
            valid = card.find('p', class_='product-card__category')
            img = card.find('img', class_='product-card__image-media').get('data-src')
            name = product_a.text.strip()
            products[k][name] = {'href': product_a.get('href'), 'img': img, 'valid': valid.text}
    
    existing_products = {p.name: p for p in Product.objects.filter(supplier=kalinko)}
    prices = extract_prices(kalinko.price_list)
    prices_keys = list(prices.keys())
    
    threshold = 80
    matches = {}
    for item_A in [name for category in products.values() for name in category]:
        best_match, best_score = None, 0
        for item_B in prices_keys:
            score = fuzz.token_set_ratio(item_A.lower(), item_B.lower())
            if score > best_score:
                best_score, best_match = score, item_B
        matches[item_A] = best_match if best_score >= threshold else 'Не найдено'
    
    for category_name, product_list in products.items():
        category_obj = Category.objects.get(name=category_name, supplier=kalinko)
        for product_name, product_data in product_list.items():
            if matches[product_name] != 'Не найдено':
                try:
                    price, bulk_price = prices[matches[product_name]]
                    if product_name in existing_products:
                        product = existing_products[product_name]
                        product.price = price
                        product.bulk_price = bulk_price
                        product.variety = product_data['valid']
                        product.image = product_data['img']
                        product.is_new = False
                        product.save()
                    else:
                        Product.objects.create(
                            name=product_name, category=category_obj, price=price,
                            variety=product_data['valid'], bulk_price=bulk_price,
                            image=product_data['img'], supplier=kalinko, is_new=True
                        )
                except Exception as e:
                    print(f"Ошибка при обработке {product_name}: {e}")

def parser_bereza(bereza):pass