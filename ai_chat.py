import tensorflow as tf
from tensorflow.keras.models import load_model

import re
import utils
import random
import textstat as t

print (tf.__version__)

modelSaveFileName = 'ytc_adopted.h5'

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

	reply, ix, ix_prob = utils.generate_a_reply2(botModel, usrInput, vocab)

	print (ix)
	print (reply)

print ('(っ・ω・）っ≡≡≡≡≡≡☆')