from django.urls import path
from .views import payment_view,payment_success
from .views import initiate_payment, payment_success, payment_failure,download_payment_pdf,payment_list_view,download_payments_csv


urlpatterns = [
    path('', payment_view, name='payment-form'),
    path('payu-initiate/', initiate_payment, name='payu-initiate'),
    path('success/', payment_success, name='payment-success'),
    path('failure/', payment_failure, name='payment-failure'),
    path('download-receipt/', download_payment_pdf, name='download-receipt'),
    path('adminpaymentsabc123secreturl/', payment_list_view, name='admin-payments'),
    path('export-payments-csv/', download_payments_csv, name='export-payments-csv'),



]













