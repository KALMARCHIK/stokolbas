from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from slugify import slugify
import json



class Feedback(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"
    
class Supplier(models.Model):
    class Meta:
        verbose_name = 'Поставщика'
        verbose_name_plural = 'Поставщики'

    name = models.CharField(verbose_name='Наименование компании', max_length=255, unique=True)
    website = models.URLField(verbose_name='Сайт компании', blank=True, null=True)
    #price_list = models.FileField(upload_to="price_lists/", blank=True, null=True, verbose_name="Прайс-лист (Excel)")
    image = models.CharField(verbose_name='Картинка', max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)  # Добавляем slug

    def __str__(self):
        return self.name

class PriceList(models.Model):
    supplier = models.ForeignKey(Supplier, related_name='pricelists', on_delete=models.CASCADE)
    file = models.FileField(upload_to="price_lists/", blank=True, null=True, verbose_name="Прайс-лист №...")

    def __str__(self):
        return self.file.name

class Category(models.Model):
    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        default_related_name = 'category'

    name = models.CharField(verbose_name='Категория', max_length=100)
    supplier = models.ForeignKey(Supplier, verbose_name='Поставщик', on_delete=models.CASCADE, related_name='category')
    image = models.CharField(verbose_name='Картинка товара', max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)  # Добавляем slug

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    supplier = models.ForeignKey(Supplier, verbose_name='Поставщик', on_delete=models.CASCADE, related_name='product')
    name = models.CharField(verbose_name='Наименование товара', max_length=255)
    price = models.IntegerField(verbose_name='Цена')
    bulk_price = models.IntegerField(verbose_name='Цена от 1000 кг')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, related_name='products')
    implementation_period = models.CharField(verbose_name='Срок реализации', max_length=1000)
    variety = models.CharField(verbose_name='Сорт', max_length=1000)
    compound = models.TextField(verbose_name='Состав')
    is_new = models.BooleanField(verbose_name='Новинка', default=False)
    image = models.CharField(verbose_name='Картинка товара', max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)  # Добавляем slug

    def __str__(self):
        return json.dumps({
            "name": self.name,
            "category": str(self.category),
            "supplier": str(self.supplier),
            "image": str(self.image),
        }, ensure_ascii=False)


class Regions(models.Model):
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    name = models.CharField(verbose_name='Регион', max_length=100)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True, blank=True)  # Добавляем slug

    def __str__(self):
        return json.dumps({
            'name': self.name,
            'description': self.description,
        }, ensure_ascii=False)


@receiver(pre_save, sender=Supplier)
@receiver(pre_save, sender=Category)
# @receiver(pre_save, sender=Product)
@receiver(pre_save, sender=Regions)
def generate_slug(sender, instance, **kwargs):
    """Универсальный сигнал для генерации slug перед сохранением модели."""
    if not instance.slug:
        instance.slug = get_unique_slug(instance)
        # print(instance.slug)


def get_unique_slug(instance, field_name="name"):
    """Функция генерации уникального slug для всех моделей."""
    print(getattr(instance, field_name, ""))
    print(slugify("Москва")) 
    slug = slugify(getattr(instance, field_name, ""))
    unique_slug = slug
    model_class = instance.__class__
    counter = 1
    # print(slug)
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    # print(unique_slug)
    return unique_slug

@receiver(pre_save, sender=Product)
def generate_product_slug(sender, instance, **kwargs):
    if not instance.slug:
        name_words = instance.name.split()
        slug_base = '-'.join(name_words[:3])  # Берем первые три слова
        generated_slug = slugify(slug_base)

        # Проверяем на уникальность
        counter = 1
        unique_slug = generated_slug
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{generated_slug}-{counter}"
            counter += 1

        instance.slug = unique_slug
        # print(instance.slug)
