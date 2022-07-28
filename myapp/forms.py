from django import forms
from myapp.models import Order, Student, Course, Image, PasswordReset


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
        fields = ('student', 'course', 'levels', 'order_date')
        widgets = {
            'student': forms.RadioSelect(),
            'order_date': forms.SelectDateWidget
        }
