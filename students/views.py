from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from payment.models import PaymentHistory
from mail.modules.welcome import WelcomeMessage
from students.forms import StudentAddForm, StudentEditForm
from userauth.forms import *
from userauth.models import *
from students.models import *
from dashboard.models import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from students.forms import StudentForm
from django.http import JsonResponse
from django.urls import reverse
from payment.forms import PaymentHistoryForm, StudentPaymentForm
import re
import pandas as pd
from datetime import datetime
from django.core.exceptions import ValidationError

EMAIL_DOMAIN = "@nathm.gov.np"


@method_decorator(csrf_exempt, name="dispatch")
class AddStudentIds(View):
    def post(self, request, *args, **kwargs):
        student_id = request.POST.get("student_id")
        college_email = request.POST.get("college_email")
        teams_id = request.POST.get("teams_id")

        # Validate email format
        if college_email and not re.match(
            rf"^[a-zA-Z0-9._%+-]+{EMAIL_DOMAIN}$", college_email
        ):
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Invalid email. It must end with {EMAIL_DOMAIN}",
                },
                status=400,
            )

        student = get_object_or_404(Student, id=student_id)

        is_sent_mail = False

        if student.college_email != college_email or student.team_id != teams_id:
            is_sent_mail = (
                college_email and student.college_email != college_email
            ) or (teams_id and student.team_id != teams_id)
            student.college_email = college_email
            student.team_id = teams_id
            student.save()

        if is_sent_mail:
            WelcomeMessage(student.user).send()

        label = "Add Ids"
        if student.college_email or student.team_id:
            label = "Update Ids"

        return JsonResponse(
            {
                "success": True,
                "message": "IDs added successfully",
                "label": label,
                "student_id": student.id,
                "email": student.college_email,
                "team_id": student.team_id,
            }
        )


class StudentView(View):
    template_name = "dashboard/students/add.html"

    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = StudentAddForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student added/updated successfully")
                return redirect("student_admin:list")
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        return render(request, self.template_name, {"form": form})

    def handle_errors(self, form):
        # Print errors for each sub-form
        form_instances = {
            "user_form": form.user_form,
            "permanent_address_form": form.permanent_address_form,
            "temporary_address_form": form.temporary_address_form,
            "payment_address_form": form.payment_address_form,
            "personal_info_form": form.personal_info_form,
            "student_form": form.student_form,
            "emergency_contact_form": form.emergency_contact_form,
            "emergency_address_form": form.emergency_address_form,
        }

        for form_name, form_instance in form_instances.items():
            print(f"{form_name} is valid: {form_instance.is_valid()}")
            if not form_instance.is_valid():
                for field, errors in form_instance.errors.items():
                    print(f"Errors for {form_name} - {field}: {errors}")


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class StudentEditView(View):
    template_name = "dashboard/students/edit.html"

    def get(self, request, *args, **kwargs):
        student_id = kwargs.pop("id", None)
        student = get_object_or_404(Student, id=student_id)

        personalinfo, created = PersonalInfo.objects.get_or_create(user=student.user)

        if not personalinfo.emergency_contact:
            emergency_contact, _ = EmergencyContact.objects.get_or_create(
                user=student.user
            )
            personalinfo.emergency_contact = emergency_contact
            personalinfo.save()

        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        form = StudentEditForm(instance=student, personalinfo_instance=personalinfo)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "student_id": student_id,
                "education_history_form": education_history_form,
                "english_test_form": english_test_form,
                "employment_history_form": employment_history_form,
            },
        )

    def post(self, request, *args, **kwargs):
        student_id = kwargs.pop("id", None)
        student = get_object_or_404(Student, id=student_id)

        personalinfo, created = PersonalInfo.objects.get_or_create(user=student.user)

        if not personalinfo.emergency_contact:
            emergency_contact = EmergencyContact.objects.create()
            personalinfo.emergency_contact = emergency_contact
            personalinfo.save()

        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        old_email = student.user.email  # Store old email before update

        form = StudentEditForm(
            data=request.POST, instance=student, personalinfo_instance=personalinfo
        )

        if form.is_valid():
            form.save()

            new_email = student.user.email

            # if new_email and (not old_email or old_email != new_email) and student.user:
            #     WelcomeMessage(
            #         student.user, email_changed=bool(old_email), old_email=old_email
            #     ).send()

            messages.success(request, "Student updated successfully")
            return redirect("student_admin:list")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "student_id": student_id,
                "education_history_form": education_history_form,
                "english_test_form": english_test_form,
                "employment_history_form": employment_history_form,
            },
        )


class StudentList(View):
    template_name = "dashboard/students/list.html"

    def get(self, request, *args, **kwargs):
        filter_by = kwargs.get("filter_by", None)
        payment_form = StudentPaymentForm()

        context = {"payment_form": payment_form, "filter_by": filter_by}

        return render(request, self.template_name, context)


class StudentAjax(View):
    def get(self, request, *args, **kwargs):
        filter_by = kwargs.get("filter_by", None)
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        campus_id = request.GET.get("campus", None)
        program_id = request.GET.get("program", None)
        department_id = request.GET.get("department", None)
        page_number = (start // length) + 1

        students = Student.objects.select_related(
            "campus", "department", "program"
        ).order_by("-id")
        if filter_by == "kiosk":
            students = students.filter(kiosk_id__isnull=False)
        elif filter_by == "admin":
            students = students.filter(kiosk_id__isnull=True)
        elif filter_by == "online":
            students = students.filter(kiosk_id="hello")

        if campus_id:
            students = students.filter(campus_id=campus_id)
        if program_id:
            students = students.filter(program_id=program_id)
        if department_id:
            students = students.filter(department_id=department_id)

        if search_value:
            students = students.filter(
                Q(user__first_name__icontains=search_value)
                | Q(user__last_name__icontains=search_value)
                | Q(student_id__icontains=search_value)
                | Q(campus__name__icontains=search_value)
                | Q(department__name__icontains=search_value)
                | Q(program__name__icontains=search_value)
            )

        paginator = Paginator(students, length)
        page_students = paginator.page(page_number)

        data = []
        for student in page_students:
            data.append(
                [
                    self.get_checkbox_html(student.id),
                    student.user.get_full_name() + "<br />" + student.user.email,
                    student.campus.name if student.campus else "",
                    student.department.name if student.department else "",
                    student.program.name if student.program else "",
                    self.get_section(student),
                    self.get_action(student),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": data,
            },
            status=200,
        )

    def get_section(self, obj):
        if obj.section:
            section_url = reverse(
                "student_admin:edit_section", kwargs={"pk": obj.section.id}
            )
            return f'<a target="_blank" href="{section_url}">{obj.section.section_name}</a>'
        return ""

    def get_checkbox_html(self, student_id):
        return (
            (
                f'<div class="form-check"><label for="checkbox_{student_id}_question"></label><input '
                f'class="form-check-input" type="checkbox" name="_selected_id"'
                f' value="{student_id}" id="checkbox_{student_id}_question"></div>'
            ),
        )

    def get_action(self, student):
        student_id = student.id
        edit_url = reverse("student_admin:edit", kwargs={"id": student_id})
        fee_url = reverse("payment:update_fee")

        if not student.college_email:
            ids_button = (
                f'<button type="button" class="btn btn-primary btn-sm addIdsModal" '
                f'data-studentid="{student_id}">Add IDs</button>'
            )
        else:
            ids_button = (
                f'<button type="button" class="btn btn-primary btn-sm addIdsModal" '
                f'data-studentid="{student_id}" data-email="{student.college_email}"'
                f' data-teamid="{student.team_id}">Update IDs</button>'
            )
        fee_button = (
            f'<button type="button" class="btn btn-primary updateFeeModal" '
            f'data-studentid="{student_id}" data-fee="{student.payment_due}">Update Fee</button>'
        )

        return f"""
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                {ids_button}
                {fee_button} 
        """


class StudentFilters(View):
    def get(self, request, *args, **kwargs):
        # Fetch filter options from the database
        campuses = list(Campus.objects.values("id", "name"))
        departments = list(Department.objects.values("id", "name"))
        programs = list(Program.objects.values("id", "name"))

        return JsonResponse(
            {
                "success": True,
                "campuses": campuses,
                "departments": departments,
                "programs": programs,
            }
        )


class KioskView(View):
    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, "dashboard/kiosk/add.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = StudentAddForm(data=request.POST)
        if form.is_valid():
            try:
                student = form.save()
                student.update_kiosk_id()
                return redirect("students:kiosk-success", pk=student.id)
            except Exception as e:
                print(e)
                messages.error(request, "Please correct the errors below.")
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)
        return render(request, "dashboard/kiosk/add.html", {"form": form})

    def handle_errors(self, form):
        form_instances = {
            "user_form": form.user_form,
            "permanent_address_form": form.permanent_address_form,
            "temporary_address_form": form.temporary_address_form,
            "payment_address_form": form.payment_address_form,
            "personal_info_form": form.personal_info_form,
            "student_form": form.student_form,
            "emergency_contact_form": form.emergency_contact_form,
            "emergency_address_form": form.emergency_address_form,
        }

        for form_name, form_instance in form_instances.items():
            print(f"{form_name} is valid: {form_instance.is_valid()}")
            if not form_instance.is_valid():
                for field, errors in form_instance.errors.items():
                    print(f"Errors for {form_name} - {field}: {errors}")


class KioskSuccessView(View):
    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, id=kwargs.get("pk"))
        return render(request, "dashboard/kiosk/success.html", {"student": student})


class EducationalHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        student = Student.objects.filter(id=kwargs.get("pk")).first()
        educations_history = EducationHistory.objects.filter(
            user=student.user
        ).order_by("-id")
        if search_value:
            educations_history = educations_history.filter(
                Q(degree_name__icontains=search_value)
                | Q(institution_name__icontains=search_value)
                | Q(graduation_year__icontains=search_value)
                | Q(major_subject__icontains=search_value)
            )

        paginator = Paginator(educations_history, length)
        educations_history = paginator.page(page_number)

        data = []
        for history in educations_history:
            data.append(
                [
                    history.degree_name,
                    history.institution_name,
                    history.graduation_year,
                    history.major_subject,
                    self.get_action(student.id, history.id, history.file),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": data,
            },
            status=200,
        )

    def get_action(self, student_id, obj_id, file):
        delete_url = reverse("generic:delete")
        backurl = reverse("student_admin:edit", kwargs={"id": student_id})

        view_file = ""
        if file and file != "None":
            view_file = f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'

        return f"""
            <form method="post" action="{delete_url}" class="button-group">
                {view_file}
                <input type="hidden" name="_selected_id" value="{obj_id}" />
                <input type="hidden" name="_selected_type" value="educational_history" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """

    def post(self, request, *args, **kwargs):
        form = EducationHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            education_history = form.save(commit=False)
            student = Student.objects.filter(id=self.kwargs["pk"]).first()
            education_history.user = student.user
            education_history.save()
            return JsonResponse(
                {"success": True, "message": "Education history added successfully."}
            )
        return JsonResponse({"errors": form.errors, "status": "error"}, status=400)


class EnglishTestHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        student = Student.objects.filter(id=kwargs.get("pk")).first()
        english_test = EnglishTest.objects.filter(user=student.user).order_by("-id")
        paginator = Paginator(english_test, length)
        english_test_history = paginator.page(page_number)

        data = []
        for history in english_test_history:
            data.append(
                [
                    history.test,
                    history.score,
                    history.date,
                    self.get_action(student.id, history.id, history.files),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": data,
            },
            status=200,
        )

    def get_action(self, student_id, obj_id, file):
        delete_url = reverse("generic:delete")
        backurl = reverse("student_admin:edit", kwargs={"id": student_id})

        view_file = ""
        if file and file != "None":
            view_file = f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'

        return f"""
            <form method="post" action="{delete_url}" class="button-group">
                {view_file}
                <input type="hidden" name="_selected_id" value="{obj_id}" />
                <input type="hidden" name="_selected_type" value="englishtest" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """

    def post(self, request, *args, **kwargs):
        form = EnglishTestForm(request.POST, request.FILES)
        if form.is_valid():
            englishtest_form = form.save(commit=False)
            student = Student.objects.filter(id=self.kwargs["pk"]).first()
            englishtest_form.user = student.user
            englishtest_form.save()
            return JsonResponse(
                {"success": True, "message": "English test saved successfully."}
            )
        return JsonResponse({"errors": form.errors, "status": "error"}, status=400)


class EmploymentHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        student = Student.objects.filter(id=kwargs.get("pk")).first()
        english_test = EmploymentHistory.objects.filter(user=student.user).order_by(
            "-id"
        )
        paginator = Paginator(english_test, length)
        english_test_history = paginator.page(page_number)

        data = []
        for history in english_test_history:
            data.append(
                [
                    history.employer_name,
                    history.title,
                    history.start_date,
                    history.end_date,
                    history.job_description,
                    self.get_action(student.id, history.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": data,
            },
            status=200,
        )

    def get_action(self, student_id, obj_id):
        delete_url = reverse("generic:delete")
        backurl = reverse("student_admin:edit", kwargs={"id": student_id})

        return f"""
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="_selected_id" value="{obj_id}" />
                <input type="hidden" name="_selected_type" value="employment_history" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """

    def post(self, request, *args, **kwargs):
        form = EmploymentHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            employment_form = form.save(commit=False)
            student = Student.objects.filter(id=self.kwargs["pk"]).first()
            employment_form.user = student.user
            employment_form.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Employment history saved saved successfully.",
                }
            )
        return JsonResponse({"errors": form.errors, "status": "error"}, status=400)


class SectionAssignUsersView(View):
    def post(self, request, *args, **kwargs):
        section_id = request.POST.get("section_id")
        user_ids = request.POST.get("user_ids", "").split(",")

        section = get_object_or_404(Sections, id=section_id)
        users = Student.objects.filter(id__in=user_ids)
        for user in users:
            user.section = section
            user.save()

        messages.success(request, "Users assigned to section successfully.")
        return JsonResponse(
            {"success": True, "message": "Users assigned to section successfully."}
        )


class SectionSelectView(View):
    def get(self, request, *args, **kwargs):
        sections = Sections.objects.order_by("-id")
        data = [{"id": section.id, "text": section.get_title()} for section in sections]

        return JsonResponse({"results": data, "pagination": {"more": False}})


class SectionView(View):
    def get(self, request, *args, **kwargs):
        draw = request.GET.get("draw")
        if draw:
            return self.get_json(request)

        section_id = kwargs.get("pk")
        if section_id:
            section = get_object_or_404(Sections, id=section_id)
            form = SectionForm(instance=section)
        else:
            form = SectionForm()
        return render(
            request, "dashboard/students/sections.html", context={"form": form}
        )

    def post(self, request, *args, **kwargs):
        section_id = kwargs.get("pk")
        if section_id:
            section = get_object_or_404(Sections, id=section_id)
            form = SectionForm(request.POST, instance=section)
        else:
            form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Section added successfully.")
            return redirect("student_admin:sections")
        return render(
            request, "dashboard/students/sections.html", context={"form": form}
        )

    def get_json(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        sections = Sections.objects.order_by("-id")
        if search_value:
            sections = sections.filter(Q(section_name__icontains=search_value))
        paginator = Paginator(sections, length)
        page_sections = paginator.page(page_number)

        data = []
        for section in page_sections:
            data.append([section.get_title(), self.get_action(section)])

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": data,
            },
            status=200,
        )

    def get_action(self, section):
        section_id = section.id
        edit_url = reverse("student_admin:edit_section", kwargs={"pk": section_id})
        delete_url = reverse("generic:delete")
        backurl = reverse("student_admin:sections")
        routine_url = reverse(
            "routine_admin:routine", kwargs={"section_id": section_id}
        )

        return f"""
                    <form method="post" action="{delete_url}" class="button-group">
                        <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                        <a href="{routine_url}" class="btn btn-warning btn-sm">Routines</a>
                        <input type="hidden" name="_selected_id" value="{section_id}" />
                        <input type="hidden" name="_selected_type" value="sections" />
                        <input type="hidden" name="_back_url" value="{backurl}" />
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                """


class UploadExcelView(View):
    template_name = "dashboard/students/list.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if not request.FILES.get("file"):
            messages.error(request, "No file uploaded.")
            return redirect("student_admin:list")

        file = request.FILES["file"]

        # Check file extension
        if not file.name.endswith((".xls", ".xlsx")):
            messages.error(
                request, "Invalid file format. Only .xls and .xlsx files are supported."
            )
            return redirect("student_admin:list")

        try:
            # Read Excel file
            df = pd.read_excel(
                file, engine="openpyxl" if file.name.endswith(".xlsx") else "xlrd"
            )
            self.process_excel_data(df)
            messages.success(
                request, "Excel file uploaded and records created successfully."
            )
        except ValidationError as e:
            messages.error(request, f"Validation Error: {e}")
        except Exception as e:
            messages.error(request, f"Error uploading file: {e}")

        return redirect("student_admin:list")

    def process_excel_data(self, df):
        df = df.fillna("")
        students = []
        student_ids = []
        existing_username = set(User.objects.values_list("username", flat=True))
        with transaction.atomic():
            for _, row in df.iterrows():
                email = str(row.get("Email") or "").strip()
                student_id = str(row.get("Student ID") or "").strip()

                # if student_id in student_ids:
                #     continue
                # student_ids.append(student_id)

                first_name = str(row.get("First Name") or "").strip()
                middle_name = str(row.get("Middle Name") or "").strip()
                last_name = str(row.get("Last Name") or "").strip()
                mobile = str(row.get("Mobile Number") or "").strip()
                citizenship_number = str(row.get("Citizenship Number") or "").strip()
                commencing_term = str(row.get("Commencing Term") or "").strip()
                scholarship_details = str(row.get("Scholarship Details") or "").strip()
                date_of_admission = self.parse_date(row.get("Date of Admission" or ""))
                date_of_birth_in_ad = self.parse_date(
                    row.get("Date of Birth in AD" or "")
                )

                # Normalize gender
                gender = str(row.get("Gender") or "").strip().lower()
                gender = gender if gender in ["male", "female", "other"] else None

                # username
                if email:
                    base_username = email.split("@")[0]
                else:
                    base_username = (
                        f"{(first_name or '')}{(last_name or '')}".strip().lower()
                    )

                base_username = base_username.replace(" ", "_")
                unique_username = base_username
                counter = 1

                while unique_username in existing_username:
                    unique_username = f"{base_username}{counter}"
                    counter += 1

                existing_username.add(unique_username)

                # Create a User object
                user = User(
                    username=unique_username,
                    email=email if email else "",
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    role="student",
                    mobile=mobile,
                )

                # Create a PersonalInfo object
                personal_info = PersonalInfo(
                    user=user,
                    gender=gender,
                    citizenship_number=citizenship_number,
                    date_of_birth_in_ad=date_of_birth_in_ad,
                )

                # Get related objects
                campus = self.get_related_object(Campus, str(row.get("Campus", "")))
                department = self.get_related_object(
                    Department, str(row.get("Department", ""))
                )
                program = self.get_related_object(Program, str(row.get("Program", "")))
                shift = self.get_valid_shift(str(row.get("Shift", "")))
                admission_officer = self.get_related_object(
                    User, str(row.get("Admission Officer", ""))
                )
                referred_by = self.get_related_object(
                    User, str(row.get("Referred By", ""))
                )
                authorize_person = self.get_related_object(
                    User, str(row.get("Authorize Person", ""))
                )

                # Create a Student object
                student = Student(
                    user=user,  # Associate with user
                    student_id=student_id,
                    campus=campus,
                    department=department,
                    program=program,
                    date_of_admission=date_of_admission,
                    shift=shift,
                    commencing_term=commencing_term,
                    scholarship_details=scholarship_details,
                    admission_officer=admission_officer,
                    referred_by=referred_by,
                    authorize_person=authorize_person,
                )

                students.append((user, personal_info, student))

            # Bulk create users first
            users = [u[0] for u in students]
            User.objects.bulk_create(users)

            # Assign created users to personal info and student objects
            for i, (user, personal_info, student) in enumerate(students):
                personal_info.user = users[i]
                student.user = users[i]

            PersonalInfo.objects.bulk_create([p[1] for p in students])
            Student.objects.bulk_create([s[2] for s in students])

            # for user in users:
            #     if user.email:
            #         WelcomeMessage(user).send()

    def get_related_object(self, model, name):
        name = (name or "").strip()
        return model.objects.filter(name=name).first() if name else None

    def parse_date(self, date_str):
        date = pd.to_datetime(date_str, errors="coerce")
        return date.date() if not pd.isnull(date) else None

    def get_valid_shift(self, shift):
        shift = (shift or "").upper()
        return shift if shift in dict(Student.SHIFT).keys() else None
