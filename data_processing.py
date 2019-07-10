import numpy as np
import re
import time
import utils


raw_data = utils.get_dataset()

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

x_shape, y_shape = utils.XY_to_train([str_x[1]], [str_y[1]], fromV, dictLen=len(vocab))

X = np.zeros(x_shape.shape, dtype=np.float32)
Y = np.zeros(y_shape.shape, dtype=np.float32)

while len(str_x) > 0:
	X_on_batch, Y_on_batch = utils.XY_to_train(str_x[:BATCH_SIZE], str_y[:BATCH_SIZE], fromV, dictLen=len(vocab))

	#print (X.shape, X_on_batch.shape)

	X = np.concatenate((X, X_on_batch), axis=0)
	Y = np.concatenate((Y, Y_on_batch), axis=0)

	#print (X, Y)
	print ('data loaded:', X[1:].shape, Y[1:].shape)
	print ('data available:', len(str_x), len(str_y))
	str_x = str_x[BATCH_SIZE:]
	str_y = str_y[BATCH_SIZE:]


utils.save_train_data('train_data.npz', X[1:], Y[1:])

print ('data saved:', X[1:].shape, Y[1:].shape)
print ('data left:', len(str_x), len(str_y))

print ('{:=^40}'.format(' data saved '))

print ('total time: {:.4f}'.format(time.time()-start))