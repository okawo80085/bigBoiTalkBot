from tflearn.data_utils import to_categorical
import tensorflow as tf
import tensorflow.keras as ker
from tensorflow.keras import layers as l

import numpy as np
import os
import re
import utils

print (tf.__version__)

def make_model():
	model = ker.Sequential()

	# input
	model.add(l.Dense(256, use_bias=False, input_shape=(2, 200, 95)))
	model.add(l.BatchNormalization())
	model.add(l.LeakyReLU())
	model.add(l.Flatten())
	

	# hidden layers


	# output
	model.add(l.Flatten())
	model.add(l.Dense(95, activation='softmax'))

	return model

generator_model = make_model()

generator_model.summary()


print ('(っ・ω・）っ≡≡≡≡≡≡☆')