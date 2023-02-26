from django import forms
from django.forms.utils import ErrorList as _ErrorList
from django.forms import HiddenInput, EmailInput, NumberInput, TimeInput, RadioSelect


class ErrorList(_ErrorList):
    template_name = 'bulma/forms/errors/p.html'


class Form(forms.Form):
    template_name_div = 'bulma/forms/div.html'
    template_name_label = 'bulma/forms/label.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = ErrorList


class ModelForm(forms.ModelForm):
    template_name_div = 'bulma/forms/div.html'
    template_name_label = 'bulma/forms/label.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = ErrorList


class TextInput(forms.TextInput):
    template_name = 'bulma/forms/widgets/input.html'


class Textarea(forms.Textarea):
    template_name = 'bulma/forms/widgets/textarea.html'


class CharField(forms.CharField):
    widget = TextInput
