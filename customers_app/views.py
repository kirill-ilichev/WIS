from django.shortcuts import render
from django.views.generic import TemplateView

from customers_app.models import Customer


class CustomersView(TemplateView):
    template_name = "customers.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        customers = Customer.objects.all()
        query_filter = self.request.GET.get('filter', None)
        if query_filter:
            customers = customers.order_by('-{}'.format(query_filter))

        context['customers'] = customers
        return context
