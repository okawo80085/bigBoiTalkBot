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
	assert model.output_shape == (None, 95)

	return model

generator_model = make_model()

generator_model.summary()

generator_model.compile(optimizer=tf.train.AdamOptimizer(0.00003),
	loss='categorical_crossentropy',
	metrics=['accuracy'])

tb_callback = tb(log_dir='.\\log\\', histogram_freq=0)

try:
	generator_model.load_weights('bigBoiAI.h5')

except Exception as e:
	print (e)
	pass

raw_data = utils.untokenize(utils.get_dataset())

vocab = sorted([chr(i) for i in range(32, 127) if i != 96])
vocab.insert(0, None)

str_x, str_y, toV, fromV = utils.dataset_to_XY(raw_data, vocab)

X, Y = utils.XY_to_train(str_x[:1000], str_y[:1000], fromV)

#print (X, Y)
print (X.shape, Y.shape)
print (len(str_x), len(str_y))

print ('='*20, 'starting training', '='*20)

generator_model.fit(X, Y, epochs=20, batch_size=500, shuffle=True, callbacks=[tb_callback])

generator_model.save('bigBoiAI.h5')

print ('='*20, 'done', '='*20)

print ('(っ・ω・）っ≡≡≡≡≡≡☆')
