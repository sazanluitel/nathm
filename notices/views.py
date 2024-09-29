from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from .forms import NoticeAddForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from .models import Notices

class NoticeAddView(View):
    def post(self, request, *args, **kwargs):
        notice_id = kwargs.get("id", None)
        
        if notice_id:
            notice = get_object_or_404(Notices, id=notice_id)
            form = NoticeAddForm(request.POST, request.FILES, instance=notice)
        else:
            form = NoticeAddForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Notice saved successfully')
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

        notices = Notices.objects.all() 
        return render(request, 'dashboard/notices/add.html', {'form': form, 'notices': notices})
    
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




