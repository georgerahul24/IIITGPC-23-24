from django import forms


class FirstCaseForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)



