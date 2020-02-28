from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ObjectMixin():
    model = None
    template = None
    pag_num = None

    def get(self, request, slug = None, username = None):
        following = None

        if slug:
            obj = get_object_or_404(self.model, slug=slug)
            obj_list = Post.objects.select_related('author', 'group').filter(group=obj).order_by("-pub_date")
        if username:
            obj = get_object_or_404(User, username=username)
            obj_list = self.model.objects.select_related('author', 'group').filter(author=obj).order_by("-pub_date")
            if request.user.is_authenticated:
                favorites = Follow.objects.select_related('author', 'user').filter(user = request.user, author__username = username).count()
                if favorites > 0:
                    following = True
        if slug == None and username == None:
            obj_list = self.model.objects.select_related('author', 'group').order_by("-pub_date").all()
            obj = None

        paginator = Paginator(obj_list, self.pag_num)
        page_number = request.GET.get('page') 
        page = paginator.get_page(page_number)
        return render(request, self.template, {'following':following, "group": obj, 'poster': obj, 'page': page, 'paginator': paginator}) 
