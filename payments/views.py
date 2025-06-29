from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Payment
from .forms import PaymentForm


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    ordering = ['-id']


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'
    success_url = reverse_lazy('payment-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Platba byla úspěšně vytvořena.'
        )
        return super().form_valid(form)


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'payments/payment_confirm_delete.html'
    success_url = reverse_lazy('payment-list')

    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            'Platba byla úspěšně smazána.'
        )
        return super().delete(request, *args, **kwargs)
