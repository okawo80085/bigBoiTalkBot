import tensorflow as tf
import tensorflow.keras as ker
from tensorflow.keras import layers as l
from tensorflow.keras.callbacks import TensorBoard as tb

import numpy as np
import re
import time
import utils

print (tf.__version__)

def make_model():
	model = ker.Sequential()

	# input
	model.add(l.Dense(2*200, use_bias=False, input_shape=(2*200,)))
	model.add(l.BatchNormalization())
	model.add(l.LeakyReLU())
	#model.add(l.Flatten())
	
	model.add(l.Reshape((1, 400)))
	assert model.output_shape == (None, 1, 400)

	# hidden layers
	model.add(l.GRU(64, return_sequences=True, activation='relu'))
	model.add(l.GRU(32, return_sequences=True, activation='relu'))
	model.add(l.GRU(32, return_sequences=True, activation='relu'))
	model.add(l.GRU(16, return_sequences=True, activation='relu'))


	# output
	model.add(l.Flatten())
	model.add(l.Dense(95, activation='softmax'))

	return model

generator_model = make_model()

generator_model.summary()

generator_model.compile(optimizer=tf.train.AdamOptimizer(0.00003),
	loss='mse',
	metrics=['accuracy'])

tb_callback = tb(log_dir='log/{}'.format(time.time()))

try:
	generator_model.load_weights('bigBoiAI.h5')

except Exception as e:
	print (e)
	pass

raw_data = utils.untokenize(utils.get_dataset())



print ('(っ・ω・）っ≡≡≡≡≡≡☆')
