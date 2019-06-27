import tensorflow as tf
from tensorflow.keras.models import load_model

import utils

print (tf.__version__)

modelSaveFileName = 'bigBoiAI.h5'

try:
	botModel = load_model(modelSaveFileName)

except Exception as e:
	print (e)
	raise Exception('failed to load model from the file \'{}\''.format(modelSaveFileName))

botModel.summary()

vocab = sorted([chr(i) for i in range(32, 127) if i != 96])
vocab.insert(0, None)

print (vocab)

while 1:
	usrInput = input('# ')

	resp, ix, ix_prob = utils.generate_a_reply(botModel, usrInput, vocab)

	print (ix)
	#print (ix_prob)
	print ([''.join(resp).strip(' ')])

print ('(っ・ω・）っ≡≡≡≡≡≡☆')