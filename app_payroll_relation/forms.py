from django import forms

class FormContasGNRE_Estados_x_Contas(forms.Form):
    conta_numero = forms.IntegerField(max_length=5, widget=forms.TextInput(
        attrs={
            "id": "conta_numero",
            "name": "conta_numero",
            "class": "form-control",
            "placeholder": "número da conta GNRE"
        }
    ))
    conta_uf = forms.CharField(max_length=14, widget=forms.TextInput(
        attrs={
            "id": "conta_uf",
            "name": "conta_uf",
            "class": "form-control",
            "placeholder": "estado da conta GNRE"
        }
    ))