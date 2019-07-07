import numpy as np
import re
import time
import utils


raw_data = utils.untokenize(utils.get_dataset())

DATA_TO_PROCESS = int(input('data to process, {} max? '.format(len(raw_data))))
BATCH_SIZE = int(input('batch size? '))

if DATA_TO_PROCESS > len(raw_data):
	DATA_TO_PROCESS = len(raw_data)

vocab = sorted([chr(i) for i in range(32, 127) if i != 96])
vocab.insert(0, None)

str_x, str_y, toV, fromV = utils.dataset_to_XY(raw_data[:DATA_TO_PROCESS], vocab)

print ('to start processing {} of data, press any key'.format(len(str_x)))
input()

x_shape, y_shape = utils.XY_to_train([str_x[1]], [str_y[1]], fromV)

X = np.zeros(x_shape.shape, dtype=np.float32)
Y = np.zeros(y_shape.shape, dtype=np.float32)

while len(str_x) > 0:
	X_on_batch, Y_on_batch = utils.XY_to_train(str_x[:BATCH_SIZE], str_y[:BATCH_SIZE], fromV)

	#print (X.shape, X_on_batch.shape)

	X = np.concatenate((X, X_on_batch), axis=0)
	Y = np.concatenate((Y, Y_on_batch), axis=0)

	#print (X, Y)
	print ('data loaded:', X.shape, Y.shape)
	print ('data available:', len(str_x), len(str_y))
	str_x = str_x[BATCH_SIZE:]
	str_y = str_y[BATCH_SIZE:]


utils.save_train_data('train_data.npz', X[1:], Y[1:])

print ('data loaded:', X.shape, Y.shape)
print ('data available:', len(str_x), len(str_y))

print ('='*20, 'data saved', '='*20)
