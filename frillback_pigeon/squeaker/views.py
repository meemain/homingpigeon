import uuid
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .apps import SqueakerConfig


import cv2
import numpy as np


def upload_image(request):
    img = request.FILES['image']
    img_extension = os.path.splitext(img.name)[-1]
    img_file = str(uuid.uuid4()) + img_extension
    return default_storage.save(settings.MEDIA_ROOT + img_file, img)

def preprocess_image(filename):
    #model expect 28x28 pixels image
    #img = SqueakerConfig.process_image('8.jpg')
    #preprocess image center image 20x20, add empty space to make 28x28, convert ot grayscale, invert image (digit should be white on black bg)
    img = cv2.imread(filename)
    grey = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grey.copy(), 75, 255, cv2.THRESH_BINARY_INV)
    _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    preprocessed_digits = []
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)

        # Creating a rectangle around the digit in the original img (for displaying the digits fetched via contours)
        cv2.rectangle(img, (x,y), (x+w, y+h), color=(0, 255, 0), thickness=2)

        # Cropping out the digit from the image corresponding to the current contours in the for loop
        digit = thresh[y:y+h, x:x+w]

        # Resizing that digit to (18, 18)
        resized_digit = cv2.resize(digit, (18,18))

        # Padding the digit with 5 pixels of black color (zeros) in each side to finally produce the image of (28, 28)
        padded_digit = np.pad(resized_digit, ((5,5),(5,5)), "constant", constant_values=0)

        # Adding the preprocessed digit to the list of preprocessed digits
        preprocessed_digits.append(padded_digit)

    return preprocessed_digits



class HousePrice(APIView):
    def get(self,request):
        if request.GET.get("rooms"):
            numb_of_rooms = request.GET.get("rooms")
            prediction = SqueakerConfig.predict_houseprice(numb_of_rooms)


            content_type = 'application/json'
            response = HttpResponse(prediction, content_type=content_type)
            response['Content-Disposition'] = ''
            return response

            # return Response({"status": request.GET.get("image_id")},   status=status.HTTP_200_OK)
        pass

import tempfile




class DetectDigitImage(APIView):
    def post(self, request, *args, **kwargs):

        result = upload_image(request=request)
        img = preprocess_image(result) #pre-process images before sending it over for prediction

        prediction = SqueakerConfig.predict_digit(img)
        content_type = 'application/json'
        response = HttpResponse(prediction, content_type=content_type)
        return response

class DetectFashionImage(APIView):
    def post(self, request, *args, **kwargs):

        result = upload_image(request=request)
        img = preprocess_image(result) #pre-process images before sending it over for prediction

        prediction = SqueakerConfig.predict_fashionitem(img)
        content_type = 'application/json'
        response = HttpResponse(prediction, content_type=content_type)
        return response


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
