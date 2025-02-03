from django.urls import path
from products.views import (
    SupplierDetailView,
    CategoryListView,
    ProductListView, 
    ProductDetailView,
    RegionsDetailView,
    ContactsView,
    BaseView,
    SupplierListView,
)

urlpatterns = [
    path('', 
        BaseView.as_view(),
        name='base-page'),
    
    path('suppliers/', 
        SupplierListView.as_view(), 
        name='supplier-list',
        ),

    # Поставщики
    path('suppliers/<slug:supplier_slug>/', 
        SupplierDetailView.as_view(), 
        name='supplier-detail',
        ),

    # Категории
    path('suppliers/<slug:supplier_slug>/products_categories/', 
        CategoryListView.as_view(), 
        name='category-list',
        ),

    # Продукты
    path('suppliers/<slug:supplier_slug>/products_categories/<slug:category_slug>/', 
        ProductListView.as_view(), 
        name='product-list',
        ),
    path('suppliers/<slug:supplier_slug>/products_categories/<slug:category_slug>/<slug:product_slug>/', 
        ProductDetailView.as_view(), 
        name='product-detail',
        ),

    # Регионы
    path('regions/<slug:regions_slug>/', 
        RegionsDetailView.as_view(), 
        name='regions-detail',
        ),

    # Контакты
    path('contacts/', 
        ContactsView.as_view(),
        name='contacts',
        )
]