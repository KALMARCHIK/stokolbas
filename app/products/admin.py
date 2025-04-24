from asyncio import (
    run as async_run,
    gather
)

from django.contrib import admin, messages
from django.db import transaction

from products.models import Supplier, Product, Category, Regions, PriceList

from parsers import parse


class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'supplier', 'name', 'category', 'is_new', 'implementation_period', 'variety', 'compound', 'price', 'bulk_price', 'image')  # Показываем имя поставщика в списке товаров
    list_filter = ('name', 'category', 'supplier')
    #actions = ['parse_selected_product_image', 'update_product_new_status']

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
        # print([i.supplier for i in queryset])
        kalinko = []
        berez = []
        pinski = []
        borisovski = []

        from parsers.kalinko_parser import kalinko_parser, save_image
        # from parsers.bereza_parser import bereza_parser
        for i in queryset:
            if i.supplier == 'Березовский мясоконсервный комбинат':
                berez.append(i)
            elif i.supplier == 'Пинский мясокомбинат':
                pinski.append(i)
            elif i.supplier == 'Калинковичский мясокомбинат':
                kalinko.append(i)
            elif i.supplier == 'Борисовский мясоконсервный комбинат':
                borisovski.append(i)
        
        kalinko_parser()
        # bereza_parser(berez)


        self.message_user(request, "Для выбранных продуктов найдены изображения!")
    # update_product_new_status.short_description = "Обновить статус новинок"
    parse_selected_product_image.short_description = "Загрузить изображения"

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier','image', 'slug')
    list_filter = ('name', 'supplier')

admin.site.register(Category, CategoryAdmin)


class PriceListInline(admin.TabularInline):
    model = PriceList
    extra = 1

async def callbyname(_id, fn):
    return _id, await fn

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'image', 'slug')
    inlines = [PriceListInline]
    actions = ["parse_selected_price_lists"]

    async def __parse_selected_price_list(self, data_to_parse):
        tasks = [callbyname(dtp['suppl_id'], parse(dtp)) for dtp in data_to_parse]
        return await gather(*tasks)

    def parse_selected_price_lists(self, request, queryset):
        """ 
        Запуск обработчика добавленных excel файлов, парсинг
        первоисточников, сопоставление данных для всех выбранных поставщиков
        """

        #self.message_user(request, "Выполняется обработка данных...", level=messages.WARNING)

        data_to_parse = []
        for q in queryset:
            data_to_parse.append({'suppl_id': q.id, 'files': [], 'url': q.website})
            for f in q.pricelists.all():
                data_to_parse[-1]['files'].append(f.file.name)

        results = async_run(self.__parse_selected_price_list(data_to_parse))

        for suppl_id, result in results:
            Product.objects.filter(supplier_id=suppl_id).delete()
            Category.objects.filter(supplier_id=suppl_id).delete()
            if result is None:
                continue
            for row in result:
                category, _ = Category.objects.get_or_create(
                    name=row['category'],
                    supplier_id=suppl_id,
                    defaults={'image': row['img']}
                )
                Product.objects.create(
                    supplier_id=suppl_id,
                    name = row['name'],
                    price = row['price'],
                    bulk_price = row['price_by_ton'],
                    category = category,
                    implementation_period = row['expiration_date'],
                    variety = '',
                    compound = row['composition'],
                    image = row['img']
                )

        self.message_user(request, "Данные обработаны!", level=messages.INFO)

    parse_selected_price_lists.short_description = "Обработать данные"

admin.site.register(Supplier, SupplierAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')

admin.site.register(Regions, RegionAdmin)
