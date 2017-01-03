import uuid
import json
from django import forms


class BaseActionForm(forms.Form):
    selection = forms.ModelMultipleChoiceField(required=False, queryset=None)
    action = forms.ChoiceField()

    empty_action_label = "--------"
    action_label = None

    def __init__(self, *args, **kwargs):
        form_uuid = str(uuid.uuid4())
        actions = kwargs.pop('actions')
        actions_queryset = kwargs.pop('actions_queryset')
        actions_fields_wrapper =  kwargs.pop('actions_fields_wrapper', None)

        actions_choices = [ (None, self.empty_action_label) ]
        actions_choices += [ (x[0],x[1]) for x in actions ]
        actions_dict = { x[0] : x[2] for x in actions }
        selection = forms.ModelMultipleChoiceField(required=False, queryset=actions_queryset)
        super(BaseActionForm, self).__init__(*args, **kwargs)

        self.fields['action'].choices = actions_choices
        if self.action_label is not None:
            self.fields['action'].label = self.action_label

        self.fields['action'].widget.attrs['data-action'] = json.dumps(actions_dict)
        if actions_fields_wrapper:
            self.fields['action'].widget.attrs['data-field-wrapper'] = actions_fields_wrapper
        self.fields['selection'].widget.attrs['data-selection'] = 1
        self.fields['selection'].queryset = actions_queryset
        for f in self.fields:
            self.fields[f].widget.attrs['data-actionform'] = form_uuid


    class Media:
        js = (
            'search_views/js/actionform.js',
        )


class ActionsListMixin(object):

    actions = []

    def after_post(self, request, *args, **kwargs):
        raise NotImplementedError("please implement after_post method for ActionsListMixin")

    def get_context_data(self, **kwargs):
        ctx = super(ActionsListMixin, self).get_context_data(**kwargs)
        ctx["action_form"] = self.actions_form_class(
            actions=self.actions, actions_queryset=self.get_queryset(),
            actions_fields_wrapper=".form-group"
        )
        return ctx

    def post(self, request, *args, **kwargs):
        """
        """
        #todo:
        #wrap in transaction
        #handle errors messages
        action_form = self.actions_form_class(
            request.POST, actions=self.actions,
            actions_queryset=self.get_queryset(),
            actions_fields_wrapper=".form-group"
        )
        action_form.is_valid()
        action = action_form.cleaned_data.get('action')
        records = action_form.cleaned_data.get('selection')
        if action:
            action_method = getattr(self, action)
            for record in records:
                action_method(record, action_form.cleaned_data)

        return self.after_post(request, *args, **kwargs)
