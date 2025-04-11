from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('email', 'amount', 'transcation_id', 'created_at','bank_transaction_id')
    readonly_fields = ('transcation_id', 'bank_transaction_id', 'created_at')
    search_fields = ('full_name', 'transcation_id','contact')
    list_filter = ('created_at',)





