from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from products.models import Supplier, Product, Category, Regions


class SupplierListView(ListView):
    model = Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        # Получаем поставщика по slug
        
        suppliers = [i for i in Supplier.objects.all()]
        return suppliers

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'supplier_detail.html'
    context_object_name = 'supplier'

    def get_object(self):
        # Получаем поставщика по slug
        return get_object_or_404(Supplier, slug=self.kwargs['supplier_slug'])
    

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # Получаем поставщика по slug
        supplier = get_object_or_404(Supplier, slug=self.kwargs['supplier_slug'])
        return Category.objects.filter(supplier=supplier)
    

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Получаем поставщика по slug
        supplier = get_object_or_404(Supplier, slug=self.kwargs['supplier_slug'])
        # Получаем категорию по slug
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'], supplier=supplier)
        return Product.objects.filter(category=category)
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        # Получаем поставщика по slug
        supplier = get_object_or_404(Supplier, slug=self.kwargs['supplier_slug'])
        # Получаем категорию по slug
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'], supplier=supplier)
        # Получаем продукт по slug и категории
        return get_object_or_404(Product, slug=self.kwargs['product_slug'], category=category)
    

class RegionsDetailView(DetailView):
    model = Regions
    template_name = 'regions_detail.html'
    context_object_name = 'region'

    def get_object(self):
        # Получаем регион по slug
        return get_object_or_404(Regions, slug=self.kwargs['regions_slug'])
    


class ContactsView(TemplateView):
    template_name = 'contacts.html'

class BaseView(TemplateView):
    template_name = 'base.html'