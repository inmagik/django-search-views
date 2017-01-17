from django.http import Http404, HttpResponse

from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.list import ListView, BaseListView
from django.views.generic.base import TemplateResponseMixin
from django.forms import ValidationError
from .filters import BaseFilter


class SearchListView(BaseListView, FormMixin, TemplateResponseMixin):
    """
    A class-based list view with a search form.
    params:
    search_fields
    order_field
    """
    #search_fields = None
    order_field = None
    allowed_orderings = []
    max_num_orderings = 3
    total_count = True

    # Allows prefetching related fields for displaying purposes (does not influence queries)
    prefetch_fields = []

    apply_distinct = False

    # Set to a list of group names for populating the user filter list combo
    #   None: -> don't filter by owner;
    #   []: -> all users except current user
    groups_for_userlist = None

    filter_class = BaseFilter

    def __init__(self, *args, **kwargs):
        self.filtering = False
        super(SearchListView, self).__init__(*args, **kwargs)


    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the search form.
        """
        update_data ={}
        sfdict = self.filter_class.get_search_fields()
        for fieldname in sfdict:
            try:
                has_multiple = sfdict[fieldname].get('multiple', False)
            except:
                has_multiple = False

            if has_multiple:
                value = self.request.GET.getlist(fieldname, [])
            else:
                value = self.request.GET.get(fieldname, None)

            update_data[fieldname] =  value

        if self.order_field:
            update_data[self.order_field] = self.request.GET.get(self.order_field, None)

        initial = self.get_initial()
        initial.update(update_data)
        kwargs = {'initial': initial }

        if self.groups_for_userlist != None:
            pot_users = User.objects.exclude(id=self.request.user.id)
            if len(self.groups_for_userlist):
                pot_users = pot_users.filter(groups__name__in = self.groups_for_userlist)
            pot_users = pot_users.distinct().order_by('username')
            user_choices = tuple([(user.id, str(user)) for user in pot_users])
            kwargs['user_choices'] = user_choices

        return kwargs

    def get_search_query(self, request):
        search_query = self.filter_class.build_q(request.GET, request)
        return search_query

    def get_order_by_fields(self, request):
        if self.order_field and self.order_field in request.GET and request.GET[self.order_field]:
            order_by = request.GET[self.order_field]
            order_by_fields = order_by.split(",")
            #order_by_fields = [x for x in order_by_fields if x.replace("-","") in [field for [field, caption] in self.allowed_orderings]]
            order_by_fields = [x for x in order_by_fields]
        else:
            order_by_fields = []
        return order_by_fields

    def get_object_list(self, request, search_errors=None):
        # From BaseListView
        search_query = self.get_search_query(request)
        order_by_fields = self.get_order_by_fields(request)
        object_list = self.get_queryset()

        if search_query:
            try:
                object_list = object_list.filter(search_query)
            except ValueError as e:
                search_errors.append(get_exception_error_msg(e))
            except ValidationError as e:
                search_errors.append(get_exception_error_msg(e))

        if order_by_fields:
            object_list = object_list.order_by(*order_by_fields)


        if self.apply_distinct:
            object_list = object_list.distinct()

        return object_list


    def get(self, request, *args, **kwargs):

        search_errors_fields = []
        search_errors = []

        # From ProcessFormMixin
        form_class = self.get_form_class()
        if form_class:
            self.form = self.get_form(form_class)
        else:
            self.form = None

        self.object_list = self.get_object_list(request, search_errors=search_errors)
        search_query = self.get_search_query(request)
        if search_query:
            self.filtering = True

        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404("Empty list and '%(class_name)s.allow_empty' is False."
                        % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        if self.total_count:
            context['total_count'] = self.get_queryset().count()


        if self.prefetch_fields:
            # Apply prefetch after pagination - otherwise it will prefetch all the related rows
            # Note: prefetch uses in (id, id, id...)
            context['object_list'] = context['object_list'].prefetch_related(*self.prefetch_fields)

        context['filtering'] = self.filtering
        context['search_errors'] = search_errors
        context['search_errors_fields'] = search_errors_fields

        order_by_fields = self.get_order_by_fields(request)
        context['order_by_fields'] = order_by_fields

        #also passing order_field and allowed_orderings
        context['order_field'] = self.order_field
        context['allowed_orderings'] = self.allowed_orderings
        context['max_num_orderings'] = min(self.max_num_orderings, len(self.allowed_orderings))


        if self.form:
            context['cleaned_data'] = self.form.fields
        else:
            context['cleaned_data'] = {}

        if len(search_errors):
            messages.add_message(self.request, messages.ERROR, ';'.join(search_errors))


        # Chance to process context after pagination
        if not 'request' in context:
            context['request'] = request
        self.before_render(context)

        return self.render_to_response(context)


    def before_render(self, context):
        """
        This method can be optionally overridden to modify the context.
        """
        return
