from .models import Category, Supplier

def global_context(request):
    return {
        'categories': Category.objects.prefetch_related('products').all(),
        'suppliers': Supplier.objects.all()
    }