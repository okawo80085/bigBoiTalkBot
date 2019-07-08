import tensorflow as tf
from tensorflow.keras.models import load_model

import numpy as np
import utils
import textstat as t
import re

print (tf.__version__)

modelSaveFileName = 'bigBoiAI_v3.1.h5'

try:
	botModel = load_model(modelSaveFileName)

except Exception as e:
	print (e)
	raise Exception('failed to load model from the file \'{}\''.format(modelSaveFileName))

botModel.summary()

vocab = utils.vocab

test_score = []

model_score = []

with open('test.txt', 'rt') as f:
	for i in f:
		in_text = utils.clean_text(i[:-1], vocab)

		resp, ix, ix_prob = utils.generate_a_reply(botModel, in_text, vocab)

		text = re.sub('[ ]+', ' ', ''.join(resp).strip(' '))

		model_score.append(t.flesch_reading_ease(text))
		test_score.append(t.flesch_reading_ease(i[:-1]))

		print (f'user: {in_text}')
		print (f'bot: {text}', '\n')


print (test_score)
print (model_score)

test_score_len = len(test_score)
print (sum(test_score)/test_score_len)

model_score_len = len(model_score)
print (sum(model_score)/model_score_len)