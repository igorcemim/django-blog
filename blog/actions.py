# coding=utf-8
from django.core.checks import messages
from django.utils.translation import gettext as _


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
