# coding=utf-8
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.conf.urls import url
from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from blog.models import GalleryImage, Gallery, Post, Config, Category
from actions import enable, duplicate, publish, unpublish
from reportlab.pdfgen import canvas
from django.http import HttpResponse


class MyAdminSite(AdminSite):

    site_header = _('Administração do Blog')
    site_title = _('Administração do Blog')
    index_title = _('Home')


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
                self.admin_site.admin_view(self.my_view, cacheable=False),
                name='blog_category_myview'
            ),
            url(
                r'^my_report/$',
                self.admin_site.admin_view(self.my_report),
                name='blog_category_report'
            ),
        ]
        return my_urls + urls

    def my_view(self, request):

        if not request.user.has_perm('blog.myview'):
            raise PermissionDenied

        context = dict(self.admin_site.each_context(request),
                       mensagem=_('Olá mundo!'))
        return TemplateResponse(request, "admin/category_myview.html", context)

    def my_report(self, request):

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="foo.pdf"'

        p = canvas.Canvas(response, bottomup=0)
        p.drawString(5, 15, _('Olá mundo!'))
        p.showPage()
        p.save()
        return response


admin.site = MyAdminSite(name='blog_admin')
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Config, ConfigAdmin)
