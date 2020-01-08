import numpy as np
import re
import time
import utils
import pickle as p
from bpe import BPE
from lose import LOSE
import tables as t
import os

import progressbar


DIR_PATH = 'data/'

SAVE_NAME = 'test.h5'
BPE_NAME = 'words3.bpe'
RAW_NAME = 'reddit_data_xy_raw.p'

bpe = BPE()
bpe.load(DIR_PATH + BPE_NAME)
endToken = bpe.str_to_token['\n']
numTokens = len(bpe.str_to_token)

lose = LOSE(fname=DIR_PATH + SAVE_NAME)

with open(DIR_PATH + RAW_NAME, 'rb') as f:
	raw_data = p.load(f)


DATA_TO_PROCESS = int(input('data to process, {} max? '.format(len(raw_data))))
BATCH_SIZE = int(input('batch size? '))

if DATA_TO_PROCESS > len(raw_data):
	DATA_TO_PROCESS = len(raw_data)

xi, xp, y = utils.encodeDataReddit(raw_data[:DATA_TO_PROCESS], bpe, endToken, low_it=True)

print ('to start processing {} of data, press any key'.format(len(xi)))
input()
print ('{:=^40}'.format(' starting '))

start = time.time()
batchCount = 0

x1_shape, x2_shape, y_shape = utils.encoded2xy(xi[:1], xp[:1], y[:1], endToken, numTokens)

Xp = np.zeros(x1_shape.shape, dtype=np.float32)
Xu = np.zeros(x2_shape.shape, dtype=np.float32)
Y = np.zeros(y_shape.shape, dtype=np.float32)

lose.newGroup(fmode='w', xp=Xp.shape[1:], xu=Xu.shape[1:], y=Y.shape[1:])

startP = len(xi)

with progressbar.ProgressBar(max_value=startP, redirect_stdout=True) as p:
	while len(xi) > 0:
		X_past_on_batch, X_user_on_batch, Y_on_batch = utils.encoded2xy(xi[:BATCH_SIZE], xp[:BATCH_SIZE], y[:BATCH_SIZE], endToken, numTokens)

		#print (X.shape, X_on_batch.shape)

		Xp = np.concatenate((Xp, X_past_on_batch), axis=0)
		Xu = np.concatenate((Xu, X_user_on_batch), axis=0)
		Y = np.concatenate((Y, Y_on_batch), axis=0)

		if batchCount % 15 == 0:
			print ('checkpoint save')
			lose.save(xp=Xp[1:], xu=Xu[1:], y=Y[1:])
			Xp = Xp[:1]
			Xu = Xu[:1]
			Y = Y[:1]

		#print (X, Y)
		#print ('data loaded:', Xp[1:].shape, Xu[1:].shape, Y[1:].shape)
		# print ('data available:', len(xi), len(xp), len(y))
		xi = xi[BATCH_SIZE:]
		xp = xp[BATCH_SIZE:]
		y = y[BATCH_SIZE:]
		batchCount += 1

		p.update(startP - len(xi))


lose.save(xp=Xp[1:], xu=Xu[1:], y=Y[1:])


print ('{:=^40}'.format(' data saved '))

#print ('data saved:', f.root.xp.shape, f.root.xu.shape, f.root.y.shape)
print ('data left:', len(xi), len(xp), len(y))


print ('(っ・ω・）っ≡≡≡≡≡≡☆')