# coding=utf-8

from django.utils.translation import gettext as _
from django.contrib import admin
from django.core.checks import messages
from blog.models import GalleryImage, Gallery, Post, Config, Category


# Duplica registros
def duplicate(self, request, queryset):

    for row in queryset:
        row.pk = None
        row.save()

        self.message_user(request, "Registro %s duplicado." % row)

duplicate.short_description = "Duplicar"


# Ativa um registro, desativa todos os outros
def enable(self, request, queryset):

    if queryset.count() > 1:
        self.message_user(
            request,
            _("Não é possível ativar múltiplos registros. Selecione apenas um registro."),
            messages.ERROR
        )
    else:
        # Desativa todos
        queryset.objects.all().update(status=False)
        # Ativa o registro selecionado
        queryset.update(status='t')
        # @TODO Customizar mensagem com label do Model
        self.message_user(request, _("Registro ativado com sucesso."))

enable.short_description = _("Ativar")


class ConfigAdmin(admin.ModelAdmin):

    list_display = ('title', 'status')
    readonly_fields = ('status',)
    actions = [enable]


class PostAdmin(admin.ModelAdmin):

    actions = [duplicate]
    list_display = ('title', 'gallery')
    search_fields = ('title', 'gallery__title',)


class GalleryImageInline(admin.TabularInline):

    model = GalleryImage
    extra = 5


class GalleryAdmin(admin.ModelAdmin):

    actions = [duplicate]
    inlines = [GalleryImageInline]


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Config, ConfigAdmin)
