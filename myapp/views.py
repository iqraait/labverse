from django.shortcuts import render, redirect
from .form import PaymentForm
import hashlib
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from .models import Payment
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Payment
from django.contrib.admin.views.decorators import staff_member_required
import csv
import datetime
from django.core.mail import EmailMessage







def get_payu_hash(data, salt):
    hash_string = f"{data['key']}|{data['txnid']}|{data['amount']}|{data['productinfo']}|{data['firstname']}|{data['email']}|||||||||||{salt}"
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()



def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payu-initiate')  # Redirect to PayU gateway
    else:
        form = PaymentForm()
    return render(request, 'myapp/first_page.html', {'form': form})




def initiate_payment(request):
    txnid = str(uuid.uuid4())[:20]
    payment = Payment.objects.latest('created_at')  # Get the latest payment record
    
    payment.transcation_id = txnid  # Assign new txnid
    payment.save()  # Save changes to DB

    data = {
        'key': settings.PAYU_MERCHANT_KEY,
        'txnid': txnid,
        'amount': str(payment.amount),
        'productinfo': 'Test Product',
        'firstname': payment.full_name, 
        'email': payment.email,     
        'phone': payment.amount,    
        'surl': request.build_absolute_uri('/success/'),
        'furl': request.build_absolute_uri('/failure/'),
        'service_provider': 'payu_paisa',
    }

    data['hash'] = get_payu_hash(data, settings.PAYU_MERCHANT_SALT)

    return render(request, 'myapp/payu_redirect.html', {
        'posted': data,
        'payu_url': settings.PAYU_BASE_URL
    })


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        payu_txn_id = request.POST.get('payuMoneyId') or request.POST.get('mihpayid')  # actual PayU transaction ID
        bank_txn_id = request.POST.get('bank_ref_num') or request.POST.get('bank_ref_no')  # Bank txn ID (key may vary)

        if email and payu_txn_id:
            try:
                payment = Payment.objects.filter(email=email).latest('created_at')
                payment.transcation_id = payu_txn_id
                payment.bank_transaction_id = bank_txn_id  # Save bank txn ID too
                payment.success=True
                payment.save()

                # # Send confirmation email
                subject = 'Payment Successful'
                message = (
                    f"Dear {payment.full_name},\n\n"
                    f"Thank you for your payment!\n\n"
                    f"Transaction ID: {payu_txn_id}\n"
                    f"Bank Transaction ID: {bank_txn_id}\n\n"
                    "Regards,\nIQRAA Hospital"
                )

                from_email = f"IQRAA HOSPITAL <{settings.EMAIL_HOST_USER}>"
                send_mail(subject, message, from_email, [email], fail_silently=False)

            except Payment.DoesNotExist:
                pass  # handle the case where no payment entry found

        return render(request, 'myapp/payment_success.html', {'data': request.POST})

    return redirect('payment-form')



def download_payment_pdf(request):
    email = request.GET.get('email', '').strip().lower()
    print(f"PDF download requested for email: {email}")
    try:
        payment = Payment.objects.filter(email=email, success=True).latest('created_at')
    except Payment.DoesNotExist:
        return HttpResponse("Payment not found.")

    template_path = 'myapp/pdf_template.html'
    context = {
        'name': payment.full_name,
        'amount': payment.amount,
        'transaction_id': payment.transcation_id,
        'date': payment.created_at  # if you have a timestamp field
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')

    return response


def payment_list_view(request):
    payments = Payment.objects.order_by('-created_at')  # Latest first
    return render(request, 'myapp/payment_list.html', {'payments': payments})


@csrf_exempt
def payment_failure(request):
    if request.method == 'POST':
        txnid = request.POST.get('txnid')

        if txnid:
            try:
                # Find the matching Payment entry
                payment = Payment.objects.get(transcation_id=txnid)
                payment.transcation_id = "no transaction processed"
                payment.success = False
                payment.save()
            except Payment.DoesNotExist:
                pass  # Handle missing txn if needed

        return render(request, 'myapp/payment_failure.html', {'data': request.POST})

    return redirect('payment-form')



def download_payments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email', 'Contact', 'Amount', 'Transaction ID', 'Bank Ref ID', 'Created At'])

    payments = Payment.objects.all().order_by('-created_at')

    for payment in payments:
        writer.writerow([
            payment.full_name,
            payment.email,
            payment.contact,
            payment.amount,
            payment.transcation_id,
            payment.bank_transaction_id,
            payment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response



# def download_receipt(request):
#     email = request.GET.get('email')

#     if not email:
#         return HttpResponse("Email is required", status=400)

#     try:
#         # Get the latest payment with this email
#         payment = Payment.objects.filter(email=email, success=True).latest('created_at')

#         context = {
#             "email": payment.email,
#             "amount": payment.amount,
#             "transaction_id": payment.transcation_id,
#             "bank_txn_id": payment.bank_transaction_id,
#             "date": payment.created_at.strftime("%Y-%m-%d %H:%M:%S")
#         }

#         html = render_to_string("myapp/recept_template.html", context)
#         result = BytesIO()
#         pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

#         if not pdf.err:
#             response = HttpResponse(result.getvalue(), content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename=receipt_{payment.transcation_id}.pdf'
#             return response
#         else:
#             return HttpResponse("Failed to generate receipt", status=500)

#     except Payment.DoesNotExist:
#         return HttpResponse("No payment found", status=404)



