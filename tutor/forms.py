from django import forms
from tutor.models import Ask

class RequestForm(forms.ModelForm):
    class Meta:
        model = Ask
        fields = ('fName', 'lName', 'subject', 'question',)
