import pandas as pd
from products.models import Product, Category

def load_category(clean_df, supplier):
    unique_categories = set(clean_df['category'].dropna().unique())  # Только уникальные значения

    existing_categories = set(Category.objects.filter(supplier=supplier).values_list('name', flat=True))

    new_categories = [Category(name=cat, supplier=supplier) for cat in unique_categories if cat not in existing_categories]

    for cat in unique_categories:
        if cat not in existing_categories:
            try:
                new_category = Category.objects.create(name=cat, supplier=supplier)
                new_categories.append(new_category)
            except Exception as e:
                print(e)

def load_price_list(clean_df, supplier):
    products = []
    
    for _, row in clean_df.iterrows():
        try:
            category_name = row.get('category')
            category_object = Category.objects.filter(name=f'{category_name}', supplier=supplier).first()
        except Exception as e:
            print(e)
        try:
            try:
                price = row.get('price')
                new_product = Product.objects.create(
                                name=row['name'],
                                weight_unit=row.get('unit', ''),  # Безопасное получение значения
                                price=price,
                                bulk_price=row.get('bulk_price', 0),
                                implementation_period = row.get('shelf_life', ''),
                                category=category_object,
                                supplier=supplier,
                                )
                new_product.append(new_product)
            except Exception as e:
                print(e)
            
        except Exception as e:
            print(e)

    
def parse_price_list(file_path, supplier_name):

    # Загружаем файл
    df = pd.read_excel(file_path, header=None)

    # Карта соответствий с поиском по ключевым словам
    columns_map = {
        'name': ['наименование'],
        'unit': ['ед', 'измер'],
        'price': ['цена', 'росс', 'руб'],
        'bulk_price': ['цена', '1000', 'кг'],
        'shelf_life': ['срок', 'реализ']
    }

    # Функция для поиска строки заголовков
    def find_header_row(df, keywords):
        for i, row in df.iterrows():
            row_str = row.astype(str).str.lower()
            if any(any(keyword in cell for keyword in keywords) for cell in row_str):
                return i
        return None

    # Поиск строки заголовков
    header_keywords = [kw for words in columns_map.values() for kw in words]
    header_row = find_header_row(df, header_keywords)

    if header_row is None:
        raise ValueError("Не удалось найти строку заголовков")

    # Устанавливаем заголовки
    df.columns = df.iloc[header_row]
    df = df.iloc[header_row + 1:].reset_index(drop=True)  # Удаляем строки выше заголовков

    # Функция для поиска наиболее подходящего столбца
    def find_best_match(col_name, mapping, used_keys):
        col_name = col_name.lower()
        for key, keywords in mapping.items():
            if key in used_keys:  # Если уже использовано, пропускаем
                continue
            if any(keyword in col_name for keyword in keywords):
                used_keys.add(key)  # Отмечаем ключ как использованный
                return key
        return None

    # Создаем новую карту сопоставления, предотвращая дублирование
    used_keys = set()
    mapped_columns = {}
    for col in df.columns:
        match = find_best_match(str(col), columns_map, used_keys)
        if match:
            mapped_columns[col] = match

    # Проверяем, есть ли 'bulk_price'
    if 'bulk_price' not in mapped_columns.values():
        print("⚠️ Внимание: 'bulk_price' не найден!")

    # Фильтруем и переименовываем столбцы
    df = df[list(mapped_columns.keys())].rename(columns=mapped_columns)

    # Убираем строки, где "Наименование" — это просто цифра
    df = df[~df['name'].astype(str).str.match(r'^\d+$')].reset_index(drop=True)

    # Определение категорий и сортов
    category = None
    processed_data = []
    for _, row in df.iterrows():
        name_value = str(row['name']).strip()

        # Проверяем, является ли строка категорией или сортом
        other_columns = row.iloc[1:].dropna().tolist()
          # При смене категории обнуляем сорт
        if len(other_columns) == 1 or other_columns == []:  
            if "сорт" in name_value.lower():  
                grade = name_value  # Это сорт
            else:
                category = name_value  # Это категория
                grade = None 
                continue 
        else:
            row_data = row.to_dict()
            row_data['category'] = category  # Добавляем текущую категорию
            processed_data.append(row_data)

    # Преобразуем в DataFrame
    clean_df = pd.DataFrame(processed_data)
    print(clean_df.head(-10))
    load_category(clean_df, supplier_name)
    load_price_list(clean_df, supplier_name)

