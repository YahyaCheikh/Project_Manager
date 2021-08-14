from django import forms
from django.db.models import fields
from django.forms import widgets
from . models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class SimpleForm(forms.Form):
    your_name = forms.CharField(label="Name", max_length=300)

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title','description'
        ]
        widgets = {
            'description': widgets.Textarea(attrs={'cols': 40, 'rows': 20}),
        }


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class TaskCompletForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','owner','estimated_durattion','is_finich_at_time','difuculty_level']
        # help_texts = {
        #     'is_finich_at_time': 'This field help us to inhrnce the occurency of our estimation',
        # }


class EntrepriseModelForm(forms.ModelForm):
    model = EntrepriseModel
    class Meta:
        fields = ['name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
            ),
            Submit('submit', 'Create')
        )
