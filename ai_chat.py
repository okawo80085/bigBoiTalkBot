import tensorflow as tf
from tensorflow.keras.models import load_model

import re
import utils
import random
import textstat as t

print (tf.__version__)

modelSaveFileName = 'bigBoiAI_v3.2.h5'

try:
	botModel = load_model(modelSaveFileName)

except Exception as e:
	print (e)
	raise Exception('failed to load model from the file \'{}\''.format(modelSaveFileName))

botModel.summary()

vocab = utils.vocab

print (vocab)

while 1:
	usrInput = utils.clean_text(input('# '), vocab)

	resps = utils.respond(botModel, usrInput, vocab)

	for i in resps:
		print (i)


print ('(っ・ω・）っ≡≡≡≡≡≡☆')