# coding: utf-8

from django.db import models


class Subdomain(models.Model):
    '''One atlas page'''
    SUBDOMAIN_STATUS = (
        (0, u'Неактивен'),
        (1, u'Активен'),)

    class Meta():
        db_table = 'subdomain'
        ordering = ['order']

    url = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50)
    isCurrent = models.BooleanField(db_column='is_current')
    status = models.SmallIntegerField(choices=SUBDOMAIN_STATUS)
    order = models.IntegerField()
    disclaimer = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def name(self):
        return self.title

    def full_url(self):
        if self.url:
            return "%s.newrynda.org" % self.url
        else:
            return "newrynda.org"


class Category(models.Model):
    ''' Категория сообщения '''
    class Meta():
        db_table = "Category"
        ordering = ['order']

    parentId = models.ForeignKey(
        'self', default=0, db_column='parent_id',
        verbose_name='Родительская категория', blank=True, null=True,
        related_name='parent')
    name = models.CharField(
        max_length=200, db_column='name',
        verbose_name='Наименование категории')
    description = models.TextField(
        blank=True, db_column='description',
        verbose_name='Описание категории')
    color = models.CharField(
        max_length=7, db_column='color',
        default='#000000', verbose_name='Цвет категории')
    slug = models.SlugField(
        max_length=255, db_column='slug',
        verbose_name='Имя для ссылки', blank=True)
    icon = models.CharField(
        max_length=255, null=True, blank=True,
        db_column='icon', verbose_name='Иконка')
    order = models.SmallIntegerField(db_column='order')
    subdomain = models.ForeignKey(
        Subdomain, null=True, blank=True,
        db_column='subdomain_id', verbose_name='Страница атласа')
    group = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Infopage(models.Model):
    class Meta():
        db_table = 'information_page'

    title = models.CharField(max_length=255, db_column='title')
    text = models.TextField(db_column='text')
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return self.title
