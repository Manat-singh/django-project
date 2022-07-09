from django import forms
from myapp.models import Order, Student, Course


class InterestForm(forms.Form):
    CHOICES = [(0, 'No'),
               (1, 'Yes')]
    interested = forms.CharField(label='Interested', widget=forms.RadioSelect(choices=CHOICES))
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(label='Additional Comments', widget=forms.Textarea, required=False)


class OrderForm(forms.ModelForm):
    student = forms.ChoiceField(widget=forms.RadioSelect, queryset=Student.objects.all())
    course = forms.ChoiceField(widget=forms.RadioSelect, queryset=Course.objects.all())
    levels = forms.IntegerField(min_value=1, initial=1)
    order_date = forms.DateField(widget=forms.SelectDateWidget)
