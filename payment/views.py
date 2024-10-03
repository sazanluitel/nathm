from django.shortcuts import render, redirect, get_object_or_404
from .views import *
from django.views import View
from payment.models import PaymentHistory
from students.models import Student
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from students.models import Sections 



# Create your views here.

class UpdateFeeView(View):
    def post(self, request, id):
        student = get_object_or_404(Student, id=id)
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        payment, created = PaymentHistory.objects.update_or_create(
            student=student,
            defaults={
                'amount': amount,
                'payment_method': payment_method,
                'status': status,
            }
        )
        return JsonResponse({'success': True})

class PaymentListView(View):
    def get(self, request):
        return render(request, 'dashboard/payment/payment_page.html')
    
class PaymentAjax(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        sections = Sections.objects.order_by("-id")
        
        # Apply search filter
        if search_value:
            sections = sections.filter(
                Q(section_name__icontains=search_value)  # Adjust based on your model
            )

        paginator = Paginator(sections, length)
        page_sections = paginator.get_page(page_number)

        data = []
        for section in page_sections:
            data.append([
                section.get_title(),
                self.get_action(section)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, section):
        section_id = section.id
        detail_url = reverse('payment:student_list_by_section', kwargs={'section_id': section_id})  # Use the new URL
        back_url = reverse('payment:payments')

        return f'''
            <div class="button-group">
                <form method="get" action="{detail_url}" style="display:inline;">
                    <input type="hidden" name="_selected_id" value="{section_id}" />
                    <input type="hidden" name="_back_url" value="{back_url}" />
                    <button type="submit" class="btn btn-secondary btn-sm">Update Fee</button>
                </form>
            </div>
        '''

class StudentListView(View):
    def get(self, request, section_id):
        section = get_object_or_404(Sections, id=section_id)
        students = Student.objects.filter(section=section)  # Assuming there's a foreign key to Sections in Student model
        return render(request, 'dashboard/payment/student_list.html', {
            'section': section,
            'students': students,
        })