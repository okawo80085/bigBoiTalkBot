import numpy as np
import re
import time
import utils

DATA_TO_PROCESS = int(input('data to process? '))

raw_data = utils.untokenize(utils.get_dataset())

vocab = sorted([chr(i) for i in range(32, 127) if i != 96])
vocab.insert(0, None)

str_x, str_y, toV, fromV = utils.dataset_to_XY(raw_data, vocab)

X, Y = utils.XY_to_train(str_x[:DATA_TO_PROCESS], str_y[:DATA_TO_PROCESS], fromV)

#print (X, Y)
print ('data loaded:', X.shape, Y.shape)
print ('data available:', len(str_x), len(str_y))


utils.save_train_data('train_data.npz', X, Y)

print ('='*20, 'data saved', '='*20)
