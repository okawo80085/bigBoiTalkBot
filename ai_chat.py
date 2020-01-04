import tensorflow as tf
from tensorflow.keras.models import load_model

import re
import utils
import random
import textstat as t
from bpe import BPE

print (tf.__version__)

modelSaveFilePath = 'modelz/ytc_adopted_bpe_edition.h5'

try:
	botModel = load_model(modelSaveFilePath)

except Exception as e:
	print (e)
	raise Exception('failed to load model from the file \'{}\''.format(modelSaveFilePath))

botModel.summary()

vocab = utils.vocab
bpe = BPE()
bpe.load('data/words2.bpe')
endToken = bpe.str_to_token['\n']

print (vocab)

while 1:
	usrInput = utils.clean_text(input('# ').lower(), vocab)
	print (bpe.encode(usrInput))
	reply, ix = utils.generate_a_reply3(botModel, usrInput, bpe, endToken)

	print (ix)
	print ([reply])

print ('(っ・ω・）っ≡≡≡≡≡≡☆')