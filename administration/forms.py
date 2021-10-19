from django import forms
from .models import Machine

# Form for tracking options
class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        exclude = ['token']