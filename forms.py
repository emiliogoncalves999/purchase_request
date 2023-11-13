from django import forms
from rekrutamentu.models import UserApplication, UserAttachment
from django.forms import inlineformset_factory
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button, Div, Field
from purchase_request.models import *






class RequestOrderForm(forms.ModelForm):
    class Meta:
        model = RequestOrder
        fields = '__all__'  # You can specify the fields you want to include if needed

    def __init__(self, *args, **kwargs):
        super(RequestOrderForm, self).__init__(*args, **kwargs)

        # Create a form helper and specify the layout
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('title', css_class='col-md-12'),

            ),

            Row(
                Column('donor', css_class='col-md-12'),

         
            ),
            Row(

                Column('routine', css_class='col-md-6'),
                Column('em_parts', css_class='col-md-6'),
            ),


            Row(
                Column('request_date', css_class='col-md-6'),
                Column('budget_limite', css_class='col-md-6'),
            ),
            
            Row(
                Column('activity', css_class='col-md-6 '),
                Column('project', css_class='col-md-6'),
            ),
            Row(
                Column('is_draft', css_class='col-md-6'),
                Column('is_urgent', css_class='col-md-6'),
            ),

            Div(
                    Button('cancel', 'Kansela', css_class='btn-secondary btn-sm', onclick="window.history.back();"),
                Submit('post', 'Submete', css_class='btn-primary btn-sm'),
            
                css_class='text-right',
            ),
        )

        # Add CSS classes to form fields if needed
        self.fields['donor'].widget.attrs['class'] = 'form-control'
        self.fields['is_urgent'].widget.attrs['class'] = 'form-control'
        self.fields['routine'].widget.attrs['class'] = 'form-control'
        self.fields['em_parts'].widget.attrs['class'] = 'form-control'
        self.fields['request_date'].widget.attrs['class'] = 'form-control'
        self.fields['budget_limite'].widget.attrs['class'] = 'form-control'
        self.fields['activity'].widget.attrs['class'] = 'form-control'
        self.fields['project'].widget.attrs['class'] = 'form-control'
        self.fields['is_draft'].widget.attrs['class'] = 'form-control'
        self.fields['request_date'].widget.input_type = 'date'


class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['quantity', 'unit', 'description', 'item_description']

    def __init__(self, *args, **kwargs):
        super(ItemRequestForm, self).__init__(*args, **kwargs)

        # Create a form helper and specify the layout
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                
                Column('item_description', css_class='col-md-4'),
                Column('quantity', css_class='col-md-4'),
                Column('unit', css_class='col-md-4'),
            ),


            Row(
                Column('description', css_class='col-md-12'),
            ),
      

            Div(
                Button('cancel', 'Kansela', css_class='btn-secondary btn-sm', onclick="window.history.back();"),
                Submit('post', 'Submete', css_class='btn-primary btn-sm'),
            
                css_class='text-right',
            ),
        )

        # Add CSS classes to form fields if needed
        self.fields['quantity'].widget.attrs['class'] = 'form-control'
        self.fields['unit'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['item_description'].widget.attrs['class'] = 'form-control'
  


class RequestOrderAproveForm(forms.ModelForm):
    class Meta:
        model = RequestOrderAprove
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super(RequestOrderAproveForm, self).__init__(*args, **kwargs)

        # Create a form helper and specify the layout
        self.helper = FormHelper()
        self.helper.layout = Layout(

  


            Row(
                Column('description', css_class='col-md-12'),
            ),
      

            Div(
                Button('cancel', 'Kansela', css_class='btn-secondary btn-sm', onclick="window.history.back();"),
                Submit('post', 'Submete', css_class='btn-primary btn-sm'),
                css_class='text-right',
            ),
        )


        self.fields['description'].widget.attrs['class'] = 'form-control'
     