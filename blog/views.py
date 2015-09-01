# coding=utf-8

from django.db.models import Count
from django.shortcuts import render
from blog.models import Post, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView


# Coisas comuns para o blog
class AbstractView(TemplateView):

    categories = None

    def dispatch(self, *args, **kwargs):

        # Inicializa a variável de categorias em todas as subclasses
        self.categories = Category.objects.annotate(post_count=Count('post'))

        return super(AbstractView, self).dispatch(*args, **kwargs)


# Coisas específicas da home
class PostsView(AbstractView):

    def get(self, request):

        filter_category = request.GET.get('category')

        # Se o filtro foi definido
        if filter_category:
            posts_list = Post.objects.filter(categories__id=filter_category)
        else:
            posts_list = Post.objects.all()

        paginator = Paginator(posts_list, 8)
        page = request.GET.get('page')

        # Trata as exceções do paginador
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'home.html', {
            'is_home': True,
            'posts': posts,
            'categories': self.categories,
        })
