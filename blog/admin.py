# coding=utf-8
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.conf.urls import url
from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.models import Permission, Group, User
from blog.models import GalleryImage, Gallery, Post, Config, Category
from actions import enable, duplicate, publish, unpublish


class MyAdminSite(AdminSite):

    site_header = 'Administração do Blog'
    site_title = 'Administração do Blog'
    index_title = 'Home'


class ConfigAdmin(admin.ModelAdmin):

    list_display = ('title', 'status')
    readonly_fields = ('status',)
    actions = [enable]
    list_filter = ('status',)


class PostAdmin(admin.ModelAdmin):

    actions = [duplicate]
    list_display = ('title', 'gallery', 'published')
    search_fields = ('title', 'gallery__title',)
    list_filter = ('published',)


class GalleryImageInline(admin.TabularInline):

    model = GalleryImage
    extra = 5


class GalleryAdmin(admin.ModelAdmin):

    list_display = ('title', 'published')
    actions = [duplicate]
    inlines = [GalleryImageInline]
    actions = [publish, unpublish]
    list_filter = ('published',)


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('title', 'published')
    actions = [publish, unpublish]
    list_filter = ('published',)

    def get_urls(self):

        urls = super(CategoryAdmin, self).get_urls()
        my_urls = [
            url(
                r'^my_view/$',
                self.admin_site.admin_view(self.my_view),
                name='blog_category_myview'
            )
        ]
        return my_urls + urls

    # @TODO Verificar permissão do usuário para acessar a view
    def my_view(self, request):

        context = dict(
           self.admin_site.each_context(request),
           mensagem=_('Olá mundo!'),
        )
        return TemplateResponse(request, "admin/category_myview.html", context)


admin.site = MyAdminSite(name='blog_admin')
admin.site.register(Permission)
admin.site.register(Group)
admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Config, ConfigAdmin)
