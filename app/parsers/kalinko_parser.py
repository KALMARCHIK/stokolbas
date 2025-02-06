import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
# from products.models import Category
import requests
import os
from django.conf import settings
from time import sleep
import slugify
from urllib.parse import urlparse

options = uc.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

def save_image(supplier, category_name, image_url):
    supplier_slug = slugify(supplier.name)
    category_slug = slugify(category_name)

    img_name = os.path.basename(urlparse(image_url).path)
    img_path = os.path.join(base_dir, img_name)

    base_dir = os.path.join(settings.MEDIA_ROOT, supplier.slug, category.slug)
    os.makedirs(base_dir, exist_ok=True)

    img_name = os.path.basename(urlparse(image_url).path)
    img_ext = os.path.splitext(img_name)[1]

    new_img_name = f"{supplier_slug}_{category_slug}{img_ext}"
    img_path = os.path.join(base_dir, new_img_name)

    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(img_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
        print(f"✅ Изображение сохранено: {img_path}")
        return f"{supplier_slug}/{category_slug}/{new_img_name}"
    else:
        print(f"❌ Ошибка загрузки: {image_url}")
        return None
    
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
    # print(category_list)
    # print(list(Category.objects.values('name')))
    for value in category_list:
        print(value)

    driver.close()

kalinko_parser()