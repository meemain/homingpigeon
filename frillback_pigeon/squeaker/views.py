from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from .apps import SqueakerConfig
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import HouseForm

def home(request):
    form = HouseForm()
    return render(request, 'squeaker/home.html', { 'houseform':form})


class call_house_model(APIView):
    def get(self,request):
        if request.method == 'GET':
            filled_form = HouseForm(request.GET)
            if filled_form.is_valid():
                created_houseform = filled_form.save()
                note = 'House price prediction:'

                #filled_form.cleaned_data['rooms']
                # get rooms from request
                numb_of_rooms = filled_form.cleaned_data['rooms']
                print('XXX', numb_of_rooms)
                #numb_of_rooms = request.GET.get('rooms')

                prediction = SqueakerConfig.predict_houseprice(numb_of_rooms)
                # build response
                response = {'house price': prediction}
                # return response
                return JsonResponse(response)


# def order(request):
#     multiple_form = MultiplePizzaForm()
#     if request.method == 'POST':
#         created_pizza_pk = None
#         filled_form = PizzaForm(request.POST)
#         if filled_form.is_valid():
#             created_pizza = filled_form.save()
#             created_pizza_pk = created_pizza.id
#             note = 'Thanks for ordering! Your %s %s and %s pizza is on its way!' %(filled_form.cleaned_data['size'], filled_form.cleaned_data['topping1'], filled_form.cleaned_data['topping2'],)
#             filled_form = PizzaForm()
#         else:
#             note = 'Order was not created, please try again'
#         new_form = PizzaForm()
#         return render(request, 'pizza/order.html', {'multiple_form':multiple_form, 'pizzaform':filled_form, 'note':note, 'created_pizza_pk':created_pizza_pk})
#     else:
#         form = PizzaForm()
#         return render(request, 'pizza/order.html', {'multiple_form':multiple_form, 'pizzaform':form})
#
#

class call_digits_model(APIView):
    def get(self,request):
        if request.method == 'GET':
            # get sound from request
            img = request.GET.get('img')

            prediction = SqueakerConfig.predict_digit(img)
            # build response
            response = {'image is': prediction}
            # return response
            return JsonResponse(response)

class call_fashion_model(APIView):
    def get(self,request):
        if request.method == 'GET':
            # get sound from request
            img = request.GET.get('img')

            prediction = SqueakerConfig.predict_fashionitem(img)
            # build response
            response = {'image is': prediction}
            # return response
            return JsonResponse(response)
