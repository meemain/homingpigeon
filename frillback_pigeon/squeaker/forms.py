from django import forms
from .models import Rooms

# class PizzaForm(forms.Form):
#     topping1 = forms.CharField(label='Topping 1', max_length=100)
#     topping2 = forms.CharField(label='Topping 2', max_length=100)
#     size = forms.ChoiceField(label='Size', choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])



class HouseForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['numb_rooms']
        labels = {'numb_rooms':"Number of Rooms"}
