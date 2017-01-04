import uuid
import json
from django import forms


class BaseActionForm(forms.Form):
    action = forms.ChoiceField()
    empty_action_label = "--------"
    action_label = None

    def __init__(self, *args, **kwargs):
        self.uuid = str(uuid.uuid4())
        actions = kwargs.pop('actions')
        actions_queryset = kwargs.pop('actions_queryset')
        actions_fields_wrapper =  kwargs.pop('actions_fields_wrapper', None)

        actions_choices = [ (None, self.empty_action_label) ]
        actions_choices += [ (x[0],x[1]) for x in actions ]
        actions_dict = { x[0] : x[2] for x in actions }

        super(BaseActionForm, self).__init__(*args, **kwargs)

        self.fields['action'].choices = actions_choices
        if self.action_label is not None:
            self.fields['action'].label = self.action_label

        self.fields['action'].widget.attrs['data-action'] = json.dumps(actions_dict)
        if actions_fields_wrapper:
            self.fields['action'].widget.attrs['data-field-wrapper'] = actions_fields_wrapper

        for f in self.fields:
            self.fields[f].widget.attrs['data-actionform'] = self.uuid


    class Media:
        js = (
            'search_views/js/actionform.js',
        )


class SelectionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.uuid = kwargs.pop('uuid')
        actions_queryset = kwargs.pop('actions_queryset')
        selection_key = kwargs.pop('selection_key')

        super(SelectionForm, self).__init__(*args, **kwargs)

        self.fields[selection_key] = forms.ModelMultipleChoiceField(required=False, queryset=None)
        self.fields[selection_key].widget.attrs['data-selection'] = 1
        self.fields[selection_key].queryset = actions_queryset
        for f in self.fields:
            self.fields[f].widget.attrs['data-actionform'] = self.uuid

        self.record_errors = {}


class ActionsListMixin(object):

    actions = []
    actions_fields_wrapper = None
    selection_key = "actions_selection"

    def after_post(self, request, *args, **kwargs):
        raise NotImplementedError("please implement after_post method for ActionsListMixin")

    def get_context_data(self, **kwargs):
        ctx = super(ActionsListMixin, self).get_context_data(**kwargs)
        qset = self.get_queryset()
        if self.request.POST:
            ctx["action_form"] = self.action_form
            ctx["selection_form"] = self.selection_form
            ctx["selection_form_pks"] = self.pks
        else:
            ctx["action_form"] = self.actions_form_class(
                actions=self.actions,
                actions_queryset=qset,
                actions_fields_wrapper=self.actions_fields_wrapper
            )
            ctx["selection_form"] = SelectionForm(
                uuid=ctx["action_form"].uuid,
                actions_queryset=qset,
                selection_key=self.selection_key
            )
            ctx["selection_form_pks"] = []


        return ctx

    def post(self, request, *args, **kwargs):
        """
        """
        #todo:
        #wrap in transaction
        #handle errors messages
        qset = self.get_queryset()
        self.action_form = self.actions_form_class(
            request.POST,
            actions=self.actions,
            actions_queryset=qset,
            actions_fields_wrapper=self.actions_fields_wrapper
        )
        self.action_form.is_valid()

        print 100, self.action_form
        action = self.action_form.cleaned_data.get('action')

        self.selection_form = SelectionForm(
            request.POST,
            uuid=self.action_form.uuid,
            actions_queryset=qset,
            selection_key=self.selection_key
        )
        self.selection_form.is_valid()


        pks = request.POST.getlist(self.selection_key)
        self.pks = [str(x) for x in pks]

        records = qset.filter(pk__in=pks)
        if action and records.exists():
            action_method = getattr(self, action)
            errors = {}
            for record in records:
                try:
                    action_method(record, self.action_form.cleaned_data)
                except Exception, e:
                    errors[record.pk] = e
            if errors.keys():
                self.selection_form.record_errors = errors

        return self.after_post(request, *args, **kwargs)
