from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import TemplateForm, CertificateForm
from django.contrib import messages
from .models import RequestCertificate
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from mail.helpers import EmailHelper  

class TemplateAddView(View):
    def post(self, request, *args, **kwargs):
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Template added successfully")
            return redirect('certificate:templates')  # Ensure 'templates' is the correct name
        return render(request, 'dashboard/certificates/templates.html', {'form': form})

    def get(self, request, **kwargs):
        form = TemplateForm()
        return render(request, 'dashboard/certificates/templates.html', {'form': form})

class CertificateRequestView(View):
    def post(self, request, **kwargs):
        form = CertificateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Certificate request submitted successfully")
            return redirect('certificate:certificatereq')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'dashboard/certificates/certificate.html', {'form': form})
        
    def get(self, request, **kwargs):
        form = CertificateForm()
        return render(request, 'dashboard/certificates/certificate.html', {'form': form})
    
class RequestCertificateAjaxView(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        certificates = RequestCertificate.objects.all()

        paginator = Paginator(certificates, length)
        page_certificates = paginator.page(page_number)

        data = []
        for certificate in page_certificates:
            data.append([
                certificate.student.email,          
                certificate.get_certificate_type_display(), 
                certificate.get_status_display(),
                self.get_action(certificate)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, certificate):
        approve_url = reverse('certificate:certificate_approve', kwargs={'id': certificate.id})
        decline_url = reverse('certificate:certificate_decline', kwargs={'id': certificate.id})

        # Approve button, disabled if already approved
        approve_button = f'''
            <a href="{approve_url}" class="btn btn-primary btn-sm">Approve</a>
        ''' if certificate.status == 'Pending' else '''
            <button class="btn btn-secondary btn-sm" disabled>Approved</button>
        '''

        # Decline button, disabled if already declined
        decline_button = f'''
            <a href="{decline_url}" class="btn btn-danger btn-sm">Decline</a>
        ''' if certificate.status == 'Pending' else '''
            <button class="btn btn-secondary btn-sm" disabled>Declined</button>
        '''

        return f'''
            <div class="button-group">
                {approve_button}
                {decline_button}
            </div>
        '''
    
class ApproveCertificateView(View):
    def post(self, request, id):
    
        certificate = get_object_or_404(RequestCertificate, id=id)
        
        # Approve the certificate
        certificate.status = 'Approved'
        certificate.is_approved = True
        certificate.save()
        messages.success(request, 'Certificate approved and email sent')
        self.send_approval_email(certificate)
       
    
    def send_approval_email(self, certificate):
        email_helper = EmailHelper()
        subject = "Your Certificate Request Has Been Approved"
        context = {
            'student_name': certificate.student.name,
            'certificate_type': certificate.certificate_type,
            'description': certificate.description,
        }
        
        pdf_filename = certificate.file
        with open(pdf_filename, 'rb') as pdf_file:
            file_content = pdf_file.read()
        
        # Attachments (filename, file_content, and MIME type for PDF)
        attachments = [(pdf_filename, file_content, 'certificate/nathm.pdf')]
        
     
        email_helper.send_with_template(
            template='certificate_approved', 
            context=context,
            subject=subject,
            to_email=certificate.student.email,
            attachments=attachments
        )

class DeclineCertificateView(View):
    def post(self, request, id):
        certificate = get_object_or_404(RequestCertificate, id=id)
        certificate.status = 'Denied'
        certificate.is_approved = False
        messages.error(request,'Certificate declined')
        certificate.save()
        
