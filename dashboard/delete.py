from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count
from assignment.models import Assignment
from notices.models import Notices
from routine.models import Routine, ExamRoutine, ExamProgramRoutine
from .forms import *
from .models import *
from userauth.models import *
from teacher.models import *
from library.models import *
from userauth.forms import *
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.db.models import Q
from students.models import *
from teacher.models import *
from django.utils.timezone import now

class DeleteHelper:
    def get_objects(self, ids, model, type_title, reverse_name=None, title_generator=None, kwargs_generator=None):
        objects = []
        objects_org = []
        try:
            for obj_id in ids:
                try:
                    obj = model.objects.get(id=obj_id)
                    title = title_generator(obj) if title_generator else obj.id
                    url = reverse(reverse_name, kwargs=kwargs_generator(obj)) if reverse_name else "#"

                    objects_org.append(obj)
                    objects.append({
                        "id": obj.id,
                        "type": type_title,
                        "title": title,
                        "url": url
                    })
                except model.DoesNotExist:
                    pass
        except Exception as e:
            print(e)
            pass
        return objects, objects_org

    def get_campus(self, ids):
        def campus_title(campus):
            return campus.name

        def campus_kwargs(campus):
            return {"id": campus.id}

        return self.get_objects(ids, Campus, "Campus", "dashboard:campusedit", campus_title, campus_kwargs)

    def get_department(self, ids):
        def department_title(department):
            return department.name

        def department_kwargs(department):
            return {"id": department.id}

        return self.get_objects(ids, Department, "Department", "dashboard:departmentedit", department_title,
                                department_kwargs)

    def get_program(self, ids):
        def program_title(program):
            return program.name

        def program_kwargs(program):
            return {"id": program.id}

        return self.get_objects(ids, Program, "Program", "dashboard:programedit", program_title, program_kwargs)

    def get_modules(self, ids):
        def modules_title(modules):
            return modules.name

        def modules_kwargs(modules):
            return {"id": modules.id}

        return self.get_objects(ids, Modules, "Modules", "dashboard:modulesedit", modules_title, modules_kwargs)

    def get_student(self, ids):
        def student_title(obj):
            return obj.user.get_full_name()

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, Student, "Student", None, student_title, student_kwargs)

    def get_educational_history(self, ids):
        def student_title(obj):
            return obj.degree_name

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, EducationHistory, "Educational History", None, student_title,
                                student_kwargs)

    def get_employment_history(self, ids):
        def student_title(obj):
            return obj.title

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, EmploymentHistory, "Employment History", None, student_title,
                                student_kwargs)

    def get_englishtest_history(self, ids):
        def student_title(obj):
            return obj.test

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, EnglishTest, "English Test", None, student_title,
                                student_kwargs)

    def get_sections(self, ids):
        def section_title(obj):
            return obj.section_name

        def section_kwargs(obj):
            return None

        return self.get_objects(ids, Sections, "Sections", None, section_title,
                                section_kwargs)

    def get_teacher(self, ids):
        def teacher_title(obj):
            return obj.user.get_full_name()

        def teacher_kwargs(obj):
            return None

        return self.get_objects(ids, Teacher, "Teacher", None, teacher_title, teacher_kwargs)

    def get_library(self, ids):
        def library_title(obj):
            return obj.book

        def library_kwargs(obj):
            return None

        return self.get_objects(ids, Library, "Library", None, library_title, library_kwargs)

    def get_book(self, ids):
        def book_title(obj):
            return obj.name

        def book_kwargs(obj):
            return None

        return self.get_objects(ids, Book, "Book", None, book_title, book_kwargs)
    def get_user(self, ids):
        def user_title(obj):
            return obj.user.get_full_name()

        def user_kwargs(obj):
            return None

        return self.get_objects(ids, User, "User", None, user_title, user_kwargs)

    def get_routines(self, ids):
        return self.get_objects(ids, Routine, "Routine")

    def get_exam_routines(self, ids):
        return self.get_objects(ids, ExamRoutine, "Routine")

    def get_examgrouproutines(self, ids):
        return self.get_objects(ids, ExamProgramRoutine, "Routines")

    def get_notices(self, ids):
        def notice_title(obj):
            return obj.name

        def notice_kwargs(obj):
            return None

        return self.get_objects(ids, Notices, "Notice", None, notice_title, notice_kwargs)

    def get_assignments(self, ids):
        def assignment_title(obj):
            return obj.title

        def assignment_kwargs(obj):
            return None

        return self.get_objects(ids, Assignment, "Assignment", None, assignment_title, assignment_kwargs)

    def get_titles(self, post_type: str, total):
        if post_type == "program":
            return "Programs" if total > 1 else "Program"
        elif post_type == "department":
            return "Departments" if total > 1 else "Department"
        elif post_type == "campus":
            return "Campuses" if total > 1 else "Campus"
        elif post_type == "modules":
            return "Modules" if total > 1 else "Module"
        elif post_type == "student":
            return "Students" if total > 1 else "Student"
        elif post_type == "teacher":
            return "Teachers" if total > 1 else "Teacher"
        elif post_type=="employment_history":
            return "Employment Histories" if total > 1 else "Employment History"
        elif post_type == "educational_history":
            return "Educational Histories" if total > 1 else "Educational History"
        elif post_type == "englishtest_history":
            return "English Test Histories" if total > 1 else "English Test History"
        elif post_type == "book":
            return "Books" if total > 1 else "Book"
        elif post_type == "Library":
            return "Libraries" if total > 1 else "Library"
        elif post_type == "User":
            return "Users" if total > 1 else "User"
        elif post_type == "routine":
            return "Routines" if total > 1 else "Routine"
        elif post_type == "exam_routine":
            return "Exam Routines" if total > 1 else "Exam Routine"
        elif post_type == "examgrouproutine":
            return "Exam Group Routines" if total > 1 else "Exam Group Routine"
        elif post_type == "notices":
            return "Notices" if total > 1 else "Notice"
        elif post_type == "assignment":
            return "Assignments" if total > 1 else "Assignment"
        elif post_type == "sections":
            return "Sections" if total > 1 else "Section"
        return "Objects"

    def get_delete_objects(self, delete_type, selected_ids=None):
        if selected_ids is None:
            selected_ids = []

        objects = []
        originals = []

        if selected_ids:
            if delete_type == "program":
                objects, originals = self.get_program(selected_ids)
            elif delete_type == "department":
                objects, originals = self.get_department(selected_ids)
            elif delete_type == "campus":
                objects, originals = self.get_campus(selected_ids)
            elif delete_type == "modules":
                objects, originals = self.get_modules(selected_ids)
            elif delete_type == "student":
                objects, originals = self.get_student(selected_ids)
            elif delete_type == "educational_history":
                objects, originals = self.get_educational_history(selected_ids)
            elif delete_type == "employment_history":
                objects, originals = self.get_employment_history(selected_ids)
            elif delete_type == "englishtest":
                objects, originals = self.get_englishtest_history(selected_ids)
            elif delete_type == "sections":
                objects, originals = self.get_sections(selected_ids)
            elif delete_type == "teacher":
                objects, originals = self.get_teacher(selected_ids)
            elif delete_type == "library":
                objects, originals = self.get_library(selected_ids)
            elif delete_type == "book":
                objects, originals = self.get_book(selected_ids)
            elif delete_type == "routine":
                objects, originals = self.get_routines(selected_ids)
            elif delete_type == "exam_routine":
                objects, originals = self.get_exam_routines(selected_ids)
            elif delete_type == "notice":
                objects, originals = self.get_notices(selected_ids)
            elif delete_type == "exam_routines":
                objects, originals = self.get_examgrouproutines(selected_ids)
            elif delete_type == "assignment":
                objects, originals = self.get_assignments(selected_ids)

        return objects, originals


class DeleteFinalView(View, DeleteHelper):
    def get(self, request, *args, **kwargs):
        return redirect("dashboard:index")

    def post(self, request, *args, **kwargs):
        delete_type = request.POST.get("_selected_type", None)
        selected_ids = request.POST.getlist("_selected_id", [])
        back = request.POST.get("_back_url", None)
        objects, originals = self.get_delete_objects(delete_type, selected_ids)

        deleted_count = 0
        for original in originals:
            try:
                original.delete()
                deleted_count += 1
            except Exception as e:
                messages.error(request, str(e))

        if deleted_count == 1:
            messages.success(request, "Successfully deleted 1 item.")
        elif deleted_count > 1:
            messages.success(request, f"Successfully deleted {deleted_count} items.")

        return redirect(back if back else "dashboard:index")


@method_decorator(csrf_exempt, name='dispatch')
class DeleteView(View, DeleteHelper):
    def post(self, request, *args, **kwargs):
        selected_ids = request.POST.getlist("_selected_id", [])
        delete_type = request.POST.get("_selected_type", None)
        back = request.POST.get("_back_url", None)
        objects, originals = self.get_delete_objects(delete_type, selected_ids)

        total_objects = len(objects)
        return render(request, 'dashboard/parts/delete.html', context={
            "objects": objects,
            "type_title": self.get_titles(delete_type, total_objects),
            "back": back,
            "type": delete_type,
            "total": total_objects
        })
