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
BATCH = 40000
LR = 0.001

SAVE_NAME = 'ytc_adopted.h5'
DATASET_PATH = 'train_data_for_adopted.npz'

startTime = time.time()

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
	#model.add(l.GRU(32, return_sequences=True, activation='relu'))

	# output
	model.add(l.Flatten())
	model.add(l.Dense(out_dim, activation='softmax'))
	assert model.output_shape == (None, out_dim)

	return model

def make_model2(input_dim=(200,), out_dim=95):
	'''
	model adopted from https://github.com/HackerPoet/YouTubeCommenter
	experimental...
	'''

	pastInput = l.Input(shape=input_dim)
	userInput = l.Input(shape=input_dim)

	#past_dense = l.Embedding(out_dim, 200, input_length=8)(pastInput)

	#user_dense = l.Dense(200)(userInput)
	#user_dense = l.LeakyReLU(0.2)(user_dense)
	#user_dense = l.RepeatVector(200)(user_dense)

	user = l.Dense(150)(userInput)
	user = l.BatchNormalization()(user)
	user = l.LeakyReLU()(user)
	user = l.RepeatVector(8)(user)

	past = l.Dense(90)(pastInput)
	past = l.BatchNormalization()(past)
	past = l.LeakyReLU()(past)
	past = l.RepeatVector(8)(past)

	x = l.concatenate([past, user])
	x = l.Dropout(0.07)(x)

	x = l.GRU(128, return_sequences=False)(x)

	out = l.Dense(out_dim, activation='softmax')(x)

	return ker.Model(inputs=[pastInput, userInput], outputs=[out])

metric = 'accuracy'

generator_model = make_model2(out_dim=len(utils.vocab))

generator_model.compile(optimizer=tf.train.AdamOptimizer(LR),
	loss='categorical_crossentropy',
	metrics=[metric])

tb_callback = tb(log_dir=os.path.normpath('./log/{}_step_{}_batch_{}'.format(SAVE_NAME, LR, BATCH)), histogram_freq=0)
generator_model.summary()

try:
	generator_model.load_weights(SAVE_NAME)

except Exception as e:
	print (e)
	pass

Xp, Xu, Y = utils.load_train_data2(DATASET_PATH)

print (Xp.shape, Xu.shape, Y.shape)

print (generator_model.predict([np.zeros((1, 200)), np.zeros((1, 200))]).shape)


print ('{:=^40}'.format('starting training'))

#batch_loss, batch_acc = generator_model.train_on_batch([Xp[:BATCH], Xu[:BATCH]], [Y[:BATCH]])

#print (batch_loss, batch_acc)

generator_model.fit([Xp, Xu], [Y], epochs=EPOCHS, batch_size=BATCH, shuffle=True, callbacks=[tb_callback])

generator_model.save(SAVE_NAME)

print ('{:=^40}'.format('done'))

print ('total time: {:.4f}s'.format(time.time()-startTime))

print ('(っ・ω・）っ≡≡≡≡≡≡☆')
