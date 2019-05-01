from django import forms
from ignis.models import *


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ("name", "file", "sharing")


class NNForm(forms.ModelForm):
    class Meta:
        model = NN
        fields = ("name", "dataset", "sharing", "code")
