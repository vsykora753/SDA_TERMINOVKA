from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['amount', 'variable_symbol', 'account_number', 'bank_code']
    search_fields = ['variable_symbol', 'account_number']
    list_filter = ['bank_code']