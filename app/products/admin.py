from django.contrib import admin
from products.models import Supplier, Product, Category, Regions
from django.db import transaction


class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'supplier', 'name', 'category', 'is_new', 'implementation_period', 'weight_unit', 'price', 'bulk_price', 'image')  # Показываем имя поставщика в списке товаров
    list_filter = ('name', 'category', 'supplier')
    actions = ['parse_selected_product_image', 'update_product_new_status']

    # def update_product_new_status(self, request, queryset):
    #     print([i.category for i in queryset])
        
    #     product_to_process = []

    #     for product in queryset:
    #         if not product.image:
    #             product_to_process.append((product.name, product.category, product))
        
    #     from parsers.site_parser import parse_new_status
    #     for product_name, product_category, product in product_to_process:
    #         parse_new_status(product_name, product_category, product)

    #     print(product_to_process)
    #     self.message_user(request, "Для выбранных продуктов обновлен статус новинок!")

    def parse_selected_product_image(self, request, queryset):
        print([i.supplier for i in queryset])
        kalinko = []
        berez = []
        pinski = []
        borisovski = []

        from parsers.kalinko_parser import kalinko_parser
        from parsers.bereza_parser import bereza_parser
        for i in queryset:
            if i.supplier == 'Березовский мясоконсервный комбинат':
                berez.append(i)
            elif i.supplier == 'Пинский мясокомбинат':
                pinski.append(i)
            elif i.supplier == 'Калинковичский мясокомбинат':
                kalinko.append(i)
            elif i.supplier == 'Борисовский мясоконсервный комбинат':
                borisovski.append(i)
        
        kalinko_parser(kalinko)
        bereza_parser(berez)


        self.message_user(request, "Для выбранных продуктов найдены изображения!")
    # update_product_new_status.short_description = "Обновить статус новинок"
    parse_selected_product_image.short_description = "Загрузить изображения"

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier','slug')
    list_filter = ('name', 'supplier')

admin.site.register(Category, CategoryAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'price_list', 'slug')
    # list_filter = ('category', 'price')
    actions = ["parse_selected_price_lists"]

    def parse_selected_price_lists(self, request, queryset):
        """Ручной запуск парсинга после полного сохранения всех данных"""

        suppliers_to_process = []

        # 🔹 1. Собираем список поставщиков с загруженными файлами
        for supplier in queryset:
            if supplier.price_list:
                suppliers_to_process.append((supplier.price_list.path, supplier))

        # 🔹 2. Запускаем обработку ТОЛЬКО после завершения транзакции
        def process_files():
            from parsers.excel_parser import parse_price_list
            for file_path, supplier_name in suppliers_to_process:
                parse_price_list(file_path, supplier_name)  # Проброс имени поставщика

        transaction.on_commit(process_files)  # Выполняем после сохранения в БД
        self.message_user(request, "Выбранные прайс-листы будут обработаны после сохранения данных!")

    parse_selected_price_lists.short_description = "Обработать прайс-листы"

admin.site.register(Supplier, SupplierAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')

admin.site.register(Regions, RegionAdmin)
