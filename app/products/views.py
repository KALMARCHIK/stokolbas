from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView, CreateView
from products.models import Supplier, Product, Category, Regions, Feedback
from products.forms import FeedbackForm
from django.urls import reverse_lazy
# from django.core.mail import send_mail
import requests
import logging 
import os

logger = logging.getLogger(__name__)


# WHATSAPP_API_URL = "https://api.whatsapp.com/send?phone=89959069468&text="

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = "feedback.html"
    success_url = reverse_lazy("feedback_success")  # Перенаправление после успешной отправки

    def form_valid(self, form):
        feedback = form.save()

        # Отправка email
        # send_mail(
        #     subject="Новая заявка на обратную связь",
        #     message=f"Имя: {feedback.name}\nТелефон: {feedback.phone}\nГород: {feedback.city}\nСообщение: {feedback.message}",
        #     from_email="jora.tzvetkov@gmail.com",
        #     recipient_list=["dasaspic46@gmail.com"]
        # )

        # Отправка в Telegram
        try:
            text = f"📩 Новая заявка!\n\n👤 Имя: {feedback.name}\n📞 Телефон: {feedback.phone}\n🏙 Город: {feedback.city}\n✉ Сообщение: {feedback.message}"
            url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
            data = {"chat_id": os.getenv('TELEGRAM_CHAT_ID'), "text": text}
            response = requests.post(url, data=data)
            response_data = response.json()
            if not response_data.get("ok"):  # Если Telegram API вернул ошибку
                logger.error(f"Ошибка Telegram API: {response_data}")
        except Exception as e:
            logger.error(f"Ошибка отправки в Telegram: {e}")

        return super().form_valid(form)

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
    
class MainPageView(ListView):
    template_name = 'main-page.html'
    model = Supplier

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] =  Category.objects.prefetch_related('products').all() 
        context['suppliers'] = Supplier.objects.prefetch_related('category').all() 
        return context

class BaseView(ListView):
    template_name = 'base.html'
    model = Supplier

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] =  Category.objects.prefetch_related('products').all() 
        context['suppliers'] = Supplier.objects.prefetch_related('category').all() 
        return context