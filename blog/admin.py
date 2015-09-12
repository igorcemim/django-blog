# coding=utf-8
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.conf.urls import url
from django.utils.translation import gettext as _
from django.contrib import admin
from django.core.checks import messages
from django.contrib.auth.models import Permission, Group, User
from blog.models import GalleryImage, Gallery, Post, Config, Category


class MyAdminSite(AdminSite):
    site_header = 'Administração do Blog'
    site_title = 'Administração do Blog'
    index_title = 'Home'


# Actions

# Despublica um registro
def unpublish(modeladmin, request, queryset):

    for row in queryset:
        mensagem = _("Registro %s despublicado.") % row
        row.published = False
        row.save()

        modeladmin.message_user(request, mensagem)

unpublish.short_description = _("Despublicar")


# Publica um registro
def publish(modeladmin, request, queryset):

    for row in queryset:
        mensagem = _("Registro %s publicado.") % row
        row.published = True
        row.save()

        modeladmin.message_user(request, mensagem)

publish.short_description = _("Publicar")


# Duplica registros
def duplicate(modeladmin, request, queryset):

    for row in queryset:
        mensagem = _("Registro %s duplicado.") % row
        row.pk = None
        row.save()

        modeladmin.message_user(request, mensagem)

duplicate.short_description = _("Duplicar")


# Ativa um registro, desativa todos os outros
def enable(modeladmin, request, queryset):

    success_message = _("Registro ativado com sucesso.")
    error_message = _("Não é possível ativar múltiplos registros." +
                      "Selecione apenas um registro.")

    if queryset.count() > 1:
        modeladmin.message_user(request, error_message, messages.ERROR)
    else:
        # Desativa todos
        modeladmin.model.objects.all().update(status=False)
        # Ativa o registro selecionado
        queryset.update(status=True)
        # @TODO Customizar mensagem com label do Model
        modeladmin.message_user(request, success_message)

enable.short_description = _("Ativar")

# Admin


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
