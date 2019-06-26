import tensorflow as tf
import tensorflow.keras as ker
from tensorflow.keras import layers as l
from tensorflow.keras.callbacks import TensorBoard as tb

import numpy as np
import re
import time
import utils

print (tf.__version__)

EPOCHS = 100
BATCH = 1000

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
	assert model.output_shape == (None, 95)

	return model

generator_model = make_model()

generator_model.summary()

generator_model.compile(optimizer=tf.train.AdamOptimizer(0.0001),
	loss='categorical_crossentropy',
	metrics=['accuracy'])

tb_callback = tb(log_dir='.\\log\\', histogram_freq=0)

try:
	generator_model.load_weights('bigBoiAI.h5')

except Exception as e:
	print (e)
	pass

X, Y = utils.load_train_data('train_data.npz')

#print (X, Y)
print (X.shape, Y.shape)

print ('='*20, 'starting training', '='*20)

generator_model.fit(X, Y, epochs=EPOCHS, batch_size=BATCH, shuffle=True, callbacks=[tb_callback])

generator_model.save('bigBoiAI.h5')

print ('='*20, 'done', '='*20)

print ('(っ・ω・）っ≡≡≡≡≡≡☆')
