from django.forms import ModelForm
from .import models
from django import forms
class NewTask(ModelForm):
    important=forms.BooleanField(required=False)
    class Meta:
        model = models.Task
        fields = ['name', 'description', 'important']
class NewSubTask(ModelForm):
    important=forms.BooleanField(required=False)
    class Meta:
        model=models.SubTask
        fields=['name','description','important']
class NewMensaje(ModelForm):
    class Meta:
        model=models.Mensaje
        fields=['Mensaje']
class NewPrivateMensaje(ModelForm):
    class Meta:
        model = models.MensajePrivado
        fields = ['mensaje']