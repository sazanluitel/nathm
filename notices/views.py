from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import NoticeAddForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from .models import Notices
from userauth.models import User


class NoticeAddView(View):
    def post(self, request, *args, **kwargs):
        notice_id = kwargs.get("id", None)

        if notice_id:
            notice = get_object_or_404(Notices, id=notice_id)
            form = NoticeAddForm(request.POST, instance=notice)
        else:
            form = NoticeAddForm(request.POST)

        if form.is_valid():
            notice = form.save()  # Just this is enough
            self.send_notice(notice)
            messages.success(request, 'Notice saved and sent successfully')
            return redirect('notices_admin_urls:add')
        else:
            messages.error(request, 'Error in the form submission')
            return render(request, 'dashboard/notices/add.html', {'form': form})

    def get(self, request, *args, **kwargs):
        notice_id = kwargs.get("id", None)

        if notice_id:
            notice = get_object_or_404(Notices, id=notice_id)
            form = NoticeAddForm(instance=notice)
        else:
            form = NoticeAddForm()

        notices = Notices.objects.all().order_by('-created_at')
        return render(request, 'dashboard/notices/add.html', {'form': form, 'notices': notices})

    def send_notice(self, notice):
        users = User.objects.all()

        if notice.recipient_type != "both":
            users = users.filter(role=notice.recipient_type)

        # Apply filters based on selected campus, department, program
        if notice.departments.exists():
            users = users.filter(
                Q(student__department__in=notice.departments.all()) |
                Q(teacher__department__in=notice.departments.all())
            )
        if notice.programs.exists():
            users = users.filter(
                Q(student__program__in=notice.programs.all()) |
                Q(teacher__program__in=notice.programs.all())
            )
        if notice.campuses.exists():
            users = users.filter(
                Q(student__campus__in=notice.campuses.all()) |
                Q(teacher__campus__in=notice.campuses.all())
            )

        users = users.distinct()

        # Simulate sending notice (replace with actual logic like Notification or email)
        for user in users:
            print(f"[Sent] Notice '{notice.name}' to {user.username} ({user.role})")


class NoticeAjaxView(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        notices = Notices.objects.order_by("-id")

        if search_value:
            notices = notices.filter(
                Q(name__icontains=search_value) |
                Q(description__icontains=search_value)
            )

        paginator = Paginator(notices, length)
        page_notices = paginator.page(page_number)

        data = []
        for notice in page_notices:
            data.append([
                notice.name,
                self.get_action(notice.id)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, notice_id):
        edit_url = reverse('notices_admin_urls:edit', kwargs={'id': notice_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('notices_admin_urls:add')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>

                <input type="hidden" name="_selected_id" value="{notice_id}" />
                <input type="hidden" name="_selected_type" value="notice" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
