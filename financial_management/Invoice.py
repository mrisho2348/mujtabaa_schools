
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # For generating PDFs
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse
from twilio.rest import Client  # For sending SMS notifications
from .models import Income_Payment, Invoice
from io import StringIO,BytesIO
from django.contrib import messages


from django.http import HttpResponse

def generate_invoice(request, payment_id):
    try:
        # Retrieve the Income_Payment object
        income_payment = get_object_or_404(Income_Payment, id=payment_id)

        # Create a PDF invoice
        pdf_content_bytes = generate_pdf_invoice(income_payment)
        
        # Convert the PDF content bytes to a string
        # pdf_content = pdf_content_bytes.decode('utf-8')
        
        # Send the PDF invoice via email
        send_invoice_email(income_payment.student.admin.email, pdf_content_bytes)

        # Send a notification via SMS
        send_sms_notification(income_payment.student.phone_number, "Your invoice has been sent.")

        # Save the invoice details (you can customize this part based on your Invoice model)
        # Assuming you have an Invoice model, you can save details here.
        invoice = Invoice(
            student=income_payment.student,
            service=income_payment.service_details,
            amount_paid=income_payment.amount_paid,
            amount_required=income_payment.service_details.amount_required,
            amount_remaining=income_payment.amount_remaining,
        )
        invoice.save()

        # Redirect to the income payments list page or wherever you want
        messages.success(request, 'Invoice generated and sent successfully.')
        return redirect('financial_management:income_payment_list')
    except Exception as e:
        # Handle any exceptions here and display an error message
        messages.error(request, f'Error generating invoice: {str(e)}')
        return redirect('financial_management:income_payment_list')  # You can redirect to an appropriate page or handle the error differently




def generate_pdf_invoice(income_payment):
    
    # Create a PDF content using a template (you need to create an invoice template)
    template_path = 'invoice/invoice_template.html'  # Replace with your actual template path
    
    context = {'income_payment': income_payment}
    template = get_template(template_path)
    pdf_content = template.render(context)
    
    # Decode the PDF content from bytes to a string
    pdf_content_str = pdf_content.encode('ISO-8859-1')

    # Generate the PDF content
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(pdf_content_str), result)

    if not pdf.err:
        return result.getvalue()
    return None

def send_invoice_email(email, pdf_content):
    # Create and send an email with the PDF attachment
    subject = 'Invoice for Payment'
    message = 'Please find attached the invoice for your payment.'
    from_email = settings.DEFAULT_FROM_EMAIL    
    recipient_list = [email]  
    print(recipient_list)  
    email_message = EmailMessage(subject, message, from_email, recipient_list)
    email_message.attach('invoice.pdf', pdf_content, 'application/pdf')
    email_message.send()

def send_sms_notification(phone_number, message):
    # Send an SMS notification using Twilio (you need to set up a Twilio account and configure it)
    twilio_account_sid = 'AC6c75ccb7e00ed2c529b0821a72335932'
    twilio_auth_token = '0a3ceaba8535b83069296e3a60ff76e8'
    twilio_phone_number = '+15103384231'
    client = Client(twilio_account_sid, twilio_auth_token)
    print(phone_number)
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=phone_number
        )
    except Exception as e:
        # Handle any errors while sending SMS
        pass

def invoice_list(request):
    # Retrieve the list of invoices
    invoices = Invoice.objects.all()

    context = {'invoices': invoices}
    return render(request, 'invoice/invoice_list.html', context)