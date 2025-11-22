from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField(label="Sélectionnez une image de poubelle")
