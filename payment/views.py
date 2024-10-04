from django.shortcuts import render, redirect, get_object_or_404
from .views import *
from django.views import View
from students.models import Student
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from students.models import Sections
from .forms import StudentPaymentForm
from django.contrib import messages


class UpdateFeeView(View):
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        form = StudentPaymentForm()

        context = {
            'pending_payment_form': form,
            'student_id': student_id,
        }
        return render(request, 'dashboard/students/list.html', context)

    def post(self, request, *args, **kwargs):
        student_id = request.POST.get('student_id', None)
        student = get_object_or_404(Student, id=student_id)
        form = StudentPaymentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Fee updated successfully")
        else:
            messages.error(request, "Unable to update fee.")

        return redirect('student_admin:list')


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
                Q(section_name__icontains=search_value)
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
    def get_section(self, section_id):
        """ Helper method to get the section object. """
        return get_object_or_404(Sections, id=section_id)

    def post(self, request, *args, **kwargs):
        section_id = kwargs.get('section_id')
        section = self.get_section(section_id)
        students = Student.objects.filter(section=section)

        for student in students:
            due = request.POST.get(f"fee_amount_{student.id}", 0)
            try:
                student.fee_due = int(due)
                student.save()
            except ValueError:
                pass
        
        messages.success(request,"Fees of this section updated successfully")
        return redirect('payment:payments')
    
    def get(self, request, section_id):
        section = self.get_section(section_id)
        students = Student.objects.filter(section=section)

        return render(request, 'dashboard/payment/student_list.html', {
            'section': section,
            'students': students
        })