import numpy as np
import re
import time
import utils
import pickle as p
from bpe import BPE

bpe = BPE()
bpe.load('data/words.bpe')
endToken = bpe.str_to_token['\n']
numTokens = len(bpe.str_to_token)

with open('reddit_data_xy_raw.p', 'rb') as f:
	raw_data = p.load(f)

#raw_data = utils.get_dataset(low_it=True)

SAVE_NAME = 'data/train_data_BPExREDDIT_edition.npz'

DATA_TO_PROCESS = int(input('data to process, {} max? '.format(len(raw_data))))
BATCH_SIZE = int(input('batch size? '))

if DATA_TO_PROCESS > len(raw_data):
	DATA_TO_PROCESS = len(raw_data)

xi, xp, y = utils.encodeDataReddit(raw_data[:DATA_TO_PROCESS], bpe, endToken)

print ('to start processing {} of data, press any key'.format(len(xi)))
input()
print ('{:=^40}'.format(' starting '))

start = time.time()

x1_shape, x2_shape, y_shape = utils.encoded2xy(xi[:1], xp[:1], y[:1], endToken, numTokens)

Xp = np.zeros(x1_shape.shape, dtype=np.float32)
Xu = np.zeros(x2_shape.shape, dtype=np.float32)
Y = np.zeros(y_shape.shape, dtype=np.float32)

while len(xi) > 0:
	X_past_on_batch, X_user_on_batch, Y_on_batch = utils.encoded2xy(xi[:BATCH_SIZE], xp[:BATCH_SIZE], y[:BATCH_SIZE], endToken, numTokens)

	#print (X.shape, X_on_batch.shape)

	Xp = np.concatenate((Xp, X_past_on_batch), axis=0)
	Xu = np.concatenate((Xu, X_user_on_batch), axis=0)
	Y = np.concatenate((Y, Y_on_batch), axis=0)

	#print (X, Y)
	print ('data loaded:', Xp[1:].shape, Xu[1:].shape, Y[1:].shape)
	print ('data available:', len(xi), len(xp), len(y))
	xi = xi[BATCH_SIZE:]
	xp = xp[BATCH_SIZE:]
	y = y[BATCH_SIZE:]

utils.save_train_data2(SAVE_NAME, Xp[1:], Xu[1:], Y[1:])
print ('{:=^40}'.format(' data saved '))

print ('data saved:', Xp[1:].shape, Xu[1:].shape, Y[1:].shape)
print ('data left:', len(xi), len(xp), len(y))


print ('total time: {:.4f}s'.format(time.time()-start))

print ('(っ・ω・）っ≡≡≡≡≡≡☆')