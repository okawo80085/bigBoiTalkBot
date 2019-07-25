import numpy as np
import re
import time
import utils


raw_data = utils.get_dataset()

SAVE_NAME = 'train_data_for_adopted.npz'

DATA_TO_PROCESS = int(input('data to process, {} max? '.format(len(raw_data))))
BATCH_SIZE = int(input('batch size? '))

if DATA_TO_PROCESS > len(raw_data):
	DATA_TO_PROCESS = len(raw_data)


vocab = utils.vocab

str_x, str_y, toV, fromV = utils.dataset_to_XY(raw_data[:DATA_TO_PROCESS], vocab)

print ('to start processing {} of data, press any key'.format(len(str_x)))
input()
print ('{:=^40}'.format(' starting '))

start = time.time()

x1_shape, x2_shape, y_shape = utils.XY_to_train2(str_x[:1], str_y[:1], fromV, dictLen=len(vocab))

Xp = np.zeros(x1_shape.shape, dtype=np.float32)
Xu = np.zeros(x2_shape.shape, dtype=np.float32)
Y = np.zeros(y_shape.shape, dtype=np.float32)

while len(str_x) > 0:
	X_past_on_batch, X_user_on_batch, Y_on_batch = utils.XY_to_train2(str_x[:BATCH_SIZE], str_y[:BATCH_SIZE], fromV, dictLen=len(vocab))

	#print (X.shape, X_on_batch.shape)

	Xp = np.concatenate((Xp, X_past_on_batch), axis=0)
	Xu = np.concatenate((Xu, X_user_on_batch), axis=0)
	Y = np.concatenate((Y, Y_on_batch), axis=0)

	#print (X, Y)
	print ('data loaded:', Xp[1:].shape, Xu[1:].shape, Y[1:].shape)
	print ('data available:', len(str_x), len(str_y))
	str_x = str_x[BATCH_SIZE:]
	str_y = str_y[BATCH_SIZE:]


utils.save_train_data2(SAVE_NAME, Xp[1:], Xu[1:], Y[1:])
print ('{:=^40}'.format(' data saved '))

print ('data saved:', Xp[1:].shape, Xu[1:].shape, Y[1:].shape)
print ('data left:', len(str_x), len(str_y))


print ('total time: {:.4f}s'.format(time.time()-start))

print ('(っ・ω・）っ≡≡≡≡≡≡☆')