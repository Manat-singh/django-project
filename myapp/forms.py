from django import forms
from myapp.models import Order, Student, Course, Image, PasswordReset,Topic


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)

class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = PasswordReset
        fields = ('username',)

class InterestForm(forms.Form):
    CHOICES = [(0, 'No'),
               (1, 'Yes')]
    interested = forms.CharField(label='Interested', widget=forms.RadioSelect(choices=CHOICES))
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(label='Additional Comments', widget=forms.Textarea, required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ( 'course', 'levels', 'order_date')
        widgets = {
            'order_date': forms.SelectDateWidget
        }

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('school', 'city', 'interested_in')
    CITY_CHOICES = [('WS', 'Windsor'),
                    ('CG', 'Calgary'),
                    ('MR', 'Montreal'),
                    ('VC', 'Vancouver')]
    school = forms.CharField(label='School', widget=forms.Textarea, max_length=50, required=False)
    city = forms.CharField(label='city', widget=forms.RadioSelect(choices=CITY_CHOICES), initial='WS')
    interested_in = forms.ModelMultipleChoiceField(
                    queryset=Topic.objects.all(),
                    widget=forms.CheckboxSelectMultiple)
