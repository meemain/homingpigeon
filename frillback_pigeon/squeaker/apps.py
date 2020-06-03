# Squeaker : a young Racing Homer from 2 to 8 weeks old
from django.apps import AppConfig
from django.conf import settings
import os
import cv2
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow import keras



#for more information check this awesome medium article :

#https://medium.com/@o.kroeger/tensorflow-mnist-and-your-own-handwritten-digits-4d1cd32bbab4

class SqueakerConfig(AppConfig):
    name = 'squeaker'
    houseprice_path = os.path.join(settings.MODELS_ROOT, 'houseprice.h5')
    digits_path = os.path.join(settings.MODELS_ROOT, '_mnist_handwritten_digits.h5')
    fashion_mnist_path = os.path.join(settings.MODELS_ROOT, 'mnist_fashion.h5')

    houseprice_model = tf.keras.models.load_model(houseprice_path)
    digits_model = tf.keras.models.load_model(digits_path)
    fashion_mnist_model = tf.keras.models.load_model(fashion_mnist_path)

    # Check models architecture
    # houseprice_model.summary()
    # digits_model.summary()
    # fashion_mnist_model.summary()

    #fiture out how to access variables within the class



    def predict_houseprice(rooms):
        rooms = float(rooms)#model expect float
        prediction = SqueakerConfig.houseprice_model.predict([rooms])
        return str(prediction[0])

    def predict_digit(processed_image):
        #model expect 28x28 pixels image
        #img = SqueakerConfig.process_image('8.jpg')
        #preprocess image center image 20x20, add empty space to make 28x28, convert ot grayscale, invert image (digit should be white on black bg)
        model = SqueakerConfig.digits_model

        for digit in processed_image:
            predict = model.predict(digit.reshape(1, 28, 28, 1))
            prediction = np.argmax(predict, axis=-1)

        return prediction


    def predict_fashionitem(processed_image):
        #model expect 28x28 pixel image
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        model = SqueakerConfig.fashion_mnist_model

        for item in processed_image:
           predict = model.predict(item.reshape(1, 28, 28, 1))
           prediction = np.argmax(predict, axis=-1)


        return str(class_names[prediction[0]])


        # img = SqueakerConfig.process_image('shoe2.jpg')
        # predict = SqueakerConfig.fashion_mnist_model.predict(img)
        # prediction = np.argmax(predict, axis=-1)
        # return str(class_names[prediction[0]])
