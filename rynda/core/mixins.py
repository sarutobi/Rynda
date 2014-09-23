# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView


class PaginatorMixin(object):
    """ Paginator line mixin. Best use with list-based mixins """

    def paginator(self, num_pages, page=1, adj_pages=2, outside_range=3):
        page = int(page)
        num_pages = int(num_pages)
        if page > num_pages:
            page = num_pages

        if page < 1:
            page = 1
        has_prev = has_next = False
        if num_pages > 1:
            if page > 1:
                has_prev = True
            if page < num_pages:
                has_next = True
        # Counts minimal pages to work
        pager_size = 2 * (outside_range + adj_pages) + 1

        # If pager_size greater than total pages - pager wil show all pages in
        # range
        if pager_size >= num_pages:
            return {
                'first': [], 'window': [n for n in range(1, num_pages + 1)],
                'last': [],  'has_prev': has_prev, 'has_next': has_next}

        # Checking page windows
        # Current page in first (low) window
        if (outside_range + adj_pages + 1) >= page:
            first = []
            window = [n for n in range(
                1, outside_range + 2 + 2 * adj_pages)
                if n > 0 and n < num_pages]
            last = [n for n in range(num_pages - outside_range, num_pages+1)]
        # Current page in middle window
        elif (num_pages - outside_range - adj_pages - 1) < page:
            first = [n for n in range(1, outside_range + 1)]
            window = [n for n in range(
                num_pages - outside_range - 2 * adj_pages + 1, num_pages + 1)]
            last = []
        # Current page in last (high) window
        else:
            first = [n for n in range(1, outside_range + 1)]
            last = [n for n in range(
                num_pages - outside_range + 1, num_pages+1)]
            window = [n for n in range(
                page - adj_pages, page + adj_pages + 1)
                if n < num_pages]
        return {
            'first': first, 'window': window, 'last': last,
            'has_prev': has_prev, 'has_next': has_next}


class QueryStringMixin(object):
    """ This mixin adds a query string to context. """

    def get_context_data(self, **kwargs):
        context = super(QueryStringMixin, self).get_context_data(**kwargs)
        context['query_string'] = u'?%s' % self.request.META['QUERY_STRING']
        return context


# class MultipleFormsMixin(FormMixin):

    # form_classes = {}

    # def get_form_classes(self):
        # return self.form_classes

    # def get_forms(self, form_classes):
        # return dict([(key, klass(**self.get_form_kwargs()))
            # for key, klass in form_classes.items()])

    # def forms_valid(self, forms):
        # return super(MultipleFormsMixin, self).form_valid(forms)

    # def forms_invalid(self, forms):
        # return self.render_to_response(self.get_context_data(forms=forms))


# class ProcessMultipleFormsView(ProcessFormView):
    # """
    # A mixin that processes multiple forms on POST.

    # Every form must be valid.
    # """

    # def get(self, request, *args, **kwargs):
        # form_classes = self.get_form_classes()
        # forms = self.get_forms(form_classes)
        # return self.render_to_response(self.get_context_data(forms=forms))

    # def post(self, request, *args, **kwargs):
        # form_classes = self.get_form_classes()
        # forms = self.get_forms(form_classes)
        # if all([form.is_valid() for form in forms.values()]):
            # return self.forms_valid(forms)
        # else:
            # return self.forms_invalid(forms)


# class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    # """ A base view for displaying several forms. """


# class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    # """ A view for displaing several forms, and rendering a template response. """


# class CreateRequestM(MultipleFormsView):
    # """ Handler for multiple forms """
    # template_name = "request_form_simple.html"
    # model = Message
    # form_classes = {
        # 'message': RequestForm,
        # 'location': LocationForm,
    # }
    # success_url = reverse_lazy('message_list')

    # def get_initial(self):
        # initial = {}
        # if self.request.user.is_authenticated():
            # initial['contact_first_name'] = self.request.user.first_name
            # initial['contact_last_name'] = self.request.user.last_name
            # initial['contact_mail'] = self.request.user.email
            # initial['contact_phone'] = self.request.user.profile.phones
        # return initial

    # def forms_valid(self, forms):
        # location = forms['location'].save(commit=False)
        # location.region_id = 64
        # location.save()
        # message = forms['message'].save(commit=False)
        # message.linked_location = location
        # if self.request.user.is_authenticated():
            # message.user = self.request.user
        # else:
            # message.user = User.objects.get(pk=settings.ANONYMOUS_USER_ID)
        # message.save()
        # return super(CreateRequestM, self).forms_valid(forms)


# class ExternalScriptsMixin(object):

    # def allow_external(self):
        # return getattr(settings, 'EXTERNAL', False)
