import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from products.models import Product, Category
from time import sleep

options = uc.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

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

# save_image()