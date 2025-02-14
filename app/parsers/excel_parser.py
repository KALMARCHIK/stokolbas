import pandas as pd
from products.models import Product, Category


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
    # print(clean_df.head(-10))


def extract_prices(file_path):
    df = pd.read_excel(file_path, None)  # Читаем все листы
    result = {}
    
    for sheet_name, sheet in df.items():
        for idx, row in sheet.iterrows():
            if "Наименование продукции" in row.values and "Цена за 1кг, Руб" in row.values and "Цена за 1кг от 1т., Руб" in row.values:
                name_col = row[row == "Наименование продукции"].index[0]
                price_col = row[row == "Цена за 1кг, Руб"].index[0]
                bulk_price_col = row[row == "Цена за 1кг от 1т., Руб"].index[0]
                
                for _, data_row in sheet.iloc[idx+1:].iterrows():
                    product_name = str(data_row[name_col]).strip()
                    price = data_row[price_col]
                    bulk_price = data_row[bulk_price_col]
                    
                    if pd.notna(product_name) and pd.notna(price) and pd.notna(bulk_price):
                        result[product_name] = [price, bulk_price]
                break  # Останавливаемся после нахождения заголовков
    
    return result

