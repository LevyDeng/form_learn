from django import forms
class AddForm(forms.Form):
    a=forms.IntegerField()
    b=forms.IntegerField()

class InputForm(forms.Form):
    username=forms.CharField(max_length=32)