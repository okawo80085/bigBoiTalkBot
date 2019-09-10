import tensorflow as tf
import tensorflow.keras as ker
from tensorflow.keras import layers as l
from tensorflow.keras.callbacks import TensorBoard as tb

import numpy as np
import re
import time
import os
import utils
from bpe import BPE
from lose import LOSE

print (tf.__version__)

EPOCHS = 10
BATCH = 40000
LR = 0.001

SAVE_PATH = 'modelz/ytc_adopted_bpe_edition.h5'
DATASET_PATH = 'data/train_data_BPExREDDIT_edition.h5'

bpe = BPE()
lose = LOSE()

startTime = time.time()
bpe.load('data/words2.bpe')
lose.fname = DATASET_PATH
lose.fmode = 'r'

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

	user = l.Dense(100)(userInput)
	user = l.BatchNormalization()(user)
	user = l.LeakyReLU()(user)
	user = l.RepeatVector(8)(user)

	past = l.Dense(125)(pastInput)
	past = l.BatchNormalization()(past)
	past = l.LeakyReLU()(past)
	past = l.RepeatVector(8)(past)

	x = l.concatenate([past, user])
	x = l.Dropout(0.11)(x)

	x = l.GRU(128, return_sequences=False)(x)

	out = l.Dense(out_dim, activation='softmax')(x)

	return ker.Model(inputs=[pastInput, userInput], outputs=[out])

metric = 'accuracy'

generator_model = make_model2(out_dim=len(bpe.str_to_token))

generator_model.compile(optimizer=tf.train.AdamOptimizer(LR),
	loss='categorical_crossentropy',
	metrics=[metric])

tb_callback = tb(log_dir=os.path.normpath('./log/{}_step_{}_batch_{}_epoch_{}'.format(SAVE_PATH, LR, BATCH, EPOCHS)), histogram_freq=0)
generator_model.summary()

try:
	generator_model.load_weights(SAVE_PATH)

except Exception as e:
	print ('failed to load model\'s weights:', e)
	pass


lose.batch_size = BATCH
lose.iterItems = [['xp', 'xu'], ['y']]
lose.iterOutput = [['input_1', 'input_2'], ['dense_2']]
lose.loopforever = True
lose.shuffle = True

step_size = lose.get_shape('xp')[0]//BATCH + 2

lose.generator_init()

print ('{:=^40}'.format('starting training'))

#generator_model.fit([Xp, Xu], [Y], epochs=EPOCHS, batch_size=BATCH, shuffle=True, callbacks=[tb_callback])

h = generator_model.fit_generator(lose.generator(), steps_per_epoch=step_size, epochs=EPOCHS, shuffle=False, callbacks=[tb_callback])

generator_model.save(SAVE_PATH)

print ('{:=^40}'.format('done'))

print ('total time: {:.4f}s'.format(time.time()-startTime))

with open('loss.log', 'at') as f:
	f.write('{}\n'.format(h.history['loss'][-1]))

print ('(っ・ω・）っ≡≡≡≡≡≡☆')
