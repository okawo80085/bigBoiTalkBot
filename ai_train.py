import tensorflow as tf
import tensorflow.keras as ker
from tensorflow.keras import layers as l
from tensorflow.keras.callbacks import TensorBoard as tb

import numpy as np
import re
import time
import os
import utils

print (tf.__version__)

EPOCHS = 100
BATCH = 51000
STEP = 0.0002

SAVE_NAME = 'bigBoiAI_v3.h5'

def make_model(input_dim=(400,), out_dim=95):
	model = ker.Sequential()

	# input
	model.add(l.Dense(2*200, use_bias=False, input_shape=input_dim))
	model.add(l.BatchNormalization())
	model.add(l.LeakyReLU())
	#model.add(l.Flatten())

	model.add(l.Reshape((1, 400)))
	assert model.output_shape == (None, 1, 400)

	# hidden layers
	model.add(l.GRU(128, return_sequences=True, activation='relu'))
	model.add(l.GRU(64, return_sequences=True, activation='relu'))
	model.add(l.GRU(64, return_sequences=True, activation='relu'))
	model.add(l.GRU(32, return_sequences=True, activation='relu'))
	model.add(l.GRU(64, return_sequences=True, activation='relu'))


	# output
	model.add(l.Flatten())
	model.add(l.Dense(out_dim, activation='softmax'))
	assert model.output_shape == (None, out_dim)

	return model

generator_model = make_model(out_dim=len(utils.vocab))

generator_model.summary()

generator_model.compile(optimizer=tf.train.AdamOptimizer(STEP),
	loss='categorical_crossentropy',
	metrics=['accuracy'])

tb_callback = tb(log_dir=os.path.normpath('./log/{}_step_{}_batch_{}'.format(SAVE_NAME, STEP, BATCH)), histogram_freq=0)

try:
	generator_model.load_weights(SAVE_NAME)

except Exception as e:
	print (e)
	pass

X, Y = utils.load_train_data('train_data_big.npz')

#print (X, Y)
print (X.shape, Y.shape)

print ('='*20, 'starting training', '='*20)

generator_model.fit(X, Y, epochs=EPOCHS, batch_size=BATCH, shuffle=True, callbacks=[tb_callback])

generator_model.save(SAVE_NAME)

print ('='*20, 'done', '='*20)

print ('(っ・ω・）っ≡≡≡≡≡≡☆')
