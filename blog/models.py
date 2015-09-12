# coding=utf-8
from django.db import models
from django.utils.translation import gettext as _


class Config(models.Model):

    title = models.CharField(_("Título do site"), max_length=200)
    status = models.BooleanField(_("Ativo"), default=False)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _("configuração")
        verbose_name_plural = _("configurações")


class Gallery(models.Model):

    date = models.DateField(_("Data"))
    title = models.CharField(_("Título"), max_length=200)
    slug = models.SlugField(_("Slug"))
    published = models.BooleanField(_("Publicado"), default=False)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _("galeria")
        verbose_name_plural = _("galerias")


class Category(models.Model):

    title = models.CharField(_("Título"), max_length=100)
    published = models.BooleanField(_("Publicado"), default=False)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = _("categoria")
        verbose_name_plural = _("categorias")
        permissions = (("myview", "View customizada"),)


class Post(models.Model):

    date = models.DateField(_("Data"))
    title = models.CharField(_("Título"), max_length=200)
    pages = models.IntegerField(_("Quantidade de páginas"))
    author = models.CharField(_("Tradutor"), max_length=200, blank=True)
    gallery = models.ForeignKey(Gallery, verbose_name=_("Galeria"))
    image = models.ImageField(_("Imagem Destaque"))
    categories = models.ManyToManyField(Category, verbose_name=_("Categorias"))
    published = models.BooleanField(_("Publicado"), default=False)

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:

        verbose_name = _("post")
        verbose_name_plural = _("posts")


class GalleryImage(models.Model):

    image = models.ImageField(_("Imagem"))
    gallery = models.ForeignKey(Gallery,
                                related_name="imagens",
                                verbose_name="Galeria")

    class Meta:
        verbose_name = _("imagem")
        verbose_name_plural = _("imagens")
