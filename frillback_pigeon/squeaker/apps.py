# Squeaker : a young Racing Homer from 2 to 8 weeks old
from django.apps import AppConfig
from django.conf import settings
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow import keras




class SqueakerConfig(AppConfig):
    name = 'squeaker'
    houseprice_path = os.path.join(settings.MODELS_ROOT, 'houseprice.h5')
    digits_path = os.path.join(settings.MODELS_ROOT, 'mnist_handwritten_digits.h5')
    fashion_mnist_path = os.path.join(settings.MODELS_ROOT, 'mnist_fashion.h5')

    print('XX model path:',houseprice_path)
    houseprice_model = tf.keras.models.load_model(houseprice_path)
    digits_model = tf.keras.models.load_model(digits_path)
    fashion_mnist_model = tf.keras.models.load_model(fashion_mnist_path)

    # Check its architecture
    houseprice_model.summary()
    digits_model.summary()
    fashion_mnist_model.summary()

    def process_image(filename):
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        print('XXX Image path:',image_path)
        #img = Image.open(image_path)
        img = image.load_img(image_path, color_mode='grayscale', target_size=(28, 28))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)

        return img

    def predict_houseprice(rooms):
        rooms = float(rooms)#model expect float
        prediction = SqueakerConfig.houseprice_model.predict([rooms])
        return str(prediction[0])

    def predict_digit(img):
        #model expect 28x28 pixels image

        img = SqueakerConfig.process_image('8.jpg')
        #model.predict_classes(testx, verbose=1)
        predict = SqueakerConfig.digits_model.predict(img)
        prediction = np.argmax(predict, axis=-1)
        print('XXX prediction:', prediction)
        return str(prediction[0])

    def predict_fashionitem(img):
        #model expect 28x28 pixel image
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        img = SqueakerConfig.process_image('shoe2.jpg')
        predict = SqueakerConfig.fashion_mnist_model.predict(img)
        prediction = np.argmax(predict, axis=-1)
        return str(class_names[prediction[0]])
