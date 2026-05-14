from django import forms

from .models import Prediction


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            )
        }
