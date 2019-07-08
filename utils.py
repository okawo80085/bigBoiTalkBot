try:
	import nltk
	from nltk.corpus import nps_chat
	from nltk.corpus import names
	from sacremoses import MosesDetokenizer

except Exception as e:
	print (e)
	print ('failed to load nltk libs, training and data processing functions may stop working')

import re
import numpy as np
import random
from tensorflow.keras.utils import to_categorical

vocab = list(' \nAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz([{}])\\/|1234567890@#$%^&*+=-_,.!?:;\'"~<>')
vocab.insert(0, None)


old_vocab = sorted([chr(i) for i in range(32, 127) if i != 96])
old_vocab.insert(0, None)

def clean_text(text, vocab):
	'''
	normalizes the string
	'''
	chars = {'\'':[u"\u0060", u"\u00B4", u"\u2018", u"\u2019"], 'a':[u"\u00C0", u"\u00C1", u"\u00C2", u"\u00C3", u"\u00C4", u"\u00C5", u"\u00E0", u"\u00E1", u"\u00E2", u"\u00E3", u"\u00E4", u"\u00E5"],
				'e':[u"\u00C8", u"\u00C9", u"\u00CA", u"\u00CB", u"\u00E8", u"\u00E9", u"\u00EA", u"\u00EB"],
				'i':[u"\u00CC", u"\u00CD", u"\u00CE", u"\u00CF", u"\u00EC", u"\u00ED", u"\u00EE", u"\u00EF"],
				'o':[u"\u00D2", u"\u00D3", u"\u00D4", u"\u00D5", u"\u00D6", u"\u00F2", u"\u00F3", u"\u00F4", u"\u00F5", u"\u00F6"],
				'u':[u"\u00DA", u"\u00DB", u"\u00DC", u"\u00DD", u"\u00FA", u"\u00FB", u"\u00FC", u"\u00FD"]}

	for gud in chars:
		for bad in chars[gud]:
			text = text.replace(bad, gud)

	if 'http' in text:
		return ''

	text = text.replace('&', ' and ')
	text = re.sub(r'\.( +\.)+', '..', text)
	#text = re.sub(r'\.\.+', ' ^ ', text)
	text = re.sub(r',+', ',', text)
	text = re.sub(r'\-+', '-', text)
	text = re.sub(r'\?+', ' ? ', text)
	text = re.sub(r'\!+', ' ! ', text)
	text = re.sub(r'\'+', "'", text)
	text = re.sub(r';+', ':', text)
	text = re.sub(r'/+', ' / ', text)
	text = re.sub(r'<+', ' < ', text)
	text = re.sub(r'>+', ' > ', text)
	text = text.replace('%', '% ')
	text = text.replace(' - ', ' : ')
	text = text.replace(' -', " - ")
	text = text.replace('- ', " - ")
	text = text.replace(" '", " ")
	text = text.replace("' ", " ")

	#for c in ".,:":
	#	text = text.replace(c + ' ', ' ' + c + ' ')

	text = re.sub(r' +', ' ', text.strip(' '))

	for i in text:
		if i not in vocab:
			text = text.replace(i, '')

	return text

def proc_text(msgObj, vocab):
	'''
	converts a Discord message object into a pre-processed string for AI
	'''
	text = str(msgObj.content)
	for i in msgObj.mentions:
		x = '<@{}>'.format(i.id)
		x2 = '<@!{}>'.format(i.id)
		if i.nick != None:
			text = re.sub(x2, '{}'.format(str(i.nick)[:5]), text)

		else:
			text = re.sub(x, '{}'.format(str(i.name)), text)

		text = re.sub('[<][@][&]\d+[>]', '', text)

	return clean_text(text, vocab)

def get_dataset():
	'''
	removes most not natural messages from the nps_chat dataset and returns it
	also replaces user ids with random names
	'''
	nameList = list(names.words())

	posts = list(nps_chat.posts())

	#removing the START, JOIN, PART messages
	while 1:
		try:
			posts.remove(['PART'])

		except Exception as e:
			pass

		try:
			posts.remove(['JOIN'])

		except Exception as e:
			pass

		try:
			posts.remove(['START'])

		except Exception as e:
			pass


		if ['PART'] not in posts and ['START'] not in posts and ['JOIN'] not in posts:
			break

	#normalization

	re_pat = re.compile('^[.][ ]ACTION[ ]')
	re_pat2 = re.compile('^[.][ ]wz')
	#re_pat3 = re.compile('^\d+ [/] [a-m] [a-zA-Z!@#$%^&*()_\\/\'";:<>,.?`~]+')
	re_pat4 = re.compile('^[.] [3-9] |^[1-2][0-9] [/] [a-m]')
	re_pat5 = re.compile('^[!] \w+|^UnScramble|^U\d+ [(] U\d+|^[:] U\d+')
	re_pat6 = re.compile('^[.] Question |^[.] Scorpio |^[.] Rooster ')
	re_pat7 = re.compile('U\d+')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)
		result = re_pat.search(to_search)

		if result != None:
			temp = i[2:-1]
			temp.insert(0, '*')
			temp.append('*')
			posts[index] = temp
			#print (posts[index])

	print ('beep')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat2.search(to_search) != None:
			#print (to_search)
			del posts[index]
			del posts[index+1]
			del posts[index+2]

	print ('bop')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat4.search(to_search) != None:
			#print (to_search)
			del posts[index]

	print ('boop')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat5.search(to_search) != None:
			#print (to_search)
			#print (' '.join(posts[index+1]))
			del posts[index]

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat6.search(to_search) != None:
			#print (to_search)
			#print (' '.join(posts[index+1]))
			posts[index] = i[3:]
			#print (posts[index])

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat7.search(to_search) != None:
			for index2, j in enumerate(i):
				if re_pat7.search(j) != None:
					posts[index][index2] = random.choice(nameList)

	print ('done')

	return posts

def untokenize(nps_chatTokenized):
	'''
	takes a tokenized nps_chat dataset and returns a string list
	'''
	detok = MosesDetokenizer(lang='en')
	return [detok.detokenize(i) for i in nps_chatTokenized]

def arr_to_vocab(arr, vocab):
	'''
	returns a provided array converted with provided vocab dict, all array elements have to be in the vocab, but not all vocab elements have to be in the input array, works with strings too
	'''
	try:
		return [vocab[i] for i in arr]

	except Exception as e:
		print (e)
		return []

def dataset_to_XY(textList, vocab, maxLen=200):
	'''
	converts text data into a "bag of words" data, also generates vocab dicts 
	'''
	to_vocab = {}
	from_vocab = {}

	for i in vocab:
		to_vocab[vocab.index(i)] = i
		from_vocab[i] = vocab.index(i)

	X = []
	Y = []

	for index, i in enumerate(textList[:-1]):
		tempY = clean_text(textList[index+1], vocab)
		tempX = clean_text(i, vocab)

		if len(tempX) <= maxLen and len(tempY) <= maxLen:
			for j in range(len(tempY)):

				X.append([tempY[:j], tempX])
				Y.append(tempY[j])

			X.append([tempY, tempX])
			Y.append(None)

	return X, Y, to_vocab, from_vocab

def pad_right(arr, maxLen):
	'''
	if arr bigger then maxLen: return arr[:maxLen]
	else: returns an arr with epmty space filled with zeros
	'''
	if arr.shape[0] >= maxLen:
		return arr[:maxLen]

	else:
		return np.concatenate((arr, np.zeros(maxLen-arr.shape[0])))

def XY_to_train(strX, strY, vocabFrom, maxLen=200, dictLen=95):
	'''
	converts "bag of words" data to model accepteble training data
	'''
	outX = np.array([np.zeros(400)], dtype=np.float32)

	dataLen = len(strY)

	print ('{:=^40}'.format(' converting data '))

	for index, i in enumerate(strX):
		temp = pad_right(np.array(arr_to_vocab(i[0], vocabFrom), dtype=np.float32), maxLen)
		temp2 = pad_right(np.array(arr_to_vocab(i[1], vocabFrom), dtype=np.float32), maxLen)

		outX = np.concatenate((outX, [np.concatenate((np.array([]), temp, temp2))]), axis=0)

		if index % 100 == 0:
			print ('{}/{} done'.format(index, dataLen))

		#print (temp.shape, temp2.shape, tempX.shape)
	
	print ('{:=^40}'.format(' done '))

	return outX[1:], to_categorical(arr_to_vocab(strY, vocabFrom), dictLen)

def save_train_data(name, x, y):
	'''
	saves training data into a file
	'''
	np.savez(name, X=x, Y=y)

def load_train_data(name):
	'''
	loads training data from a file, must be a file generated by save_train_data()
	'''
	data = np.load(name)
	return data['X'], data['Y']

def find_dominant_neuron(tensor_1D):
	'''
	finds a dominant neuron and returns its probabillity and index
	'''
	neuron_index = np.argmax(tensor_1D)

	return [neuron_index, tensor_1D[neuron_index]]

def generate_a_reply(model, textInput, vocab, maxLen=200):
	'''
	generates a reply to user's input
	'''
	_, _, vocabTo, vocabFrom = dataset_to_XY([], vocab)

	out1 = []
	out2 = []

	temp2 = pad_right(np.array(arr_to_vocab(textInput, vocabFrom), dtype=np.float32), maxLen)

	while 1:

		if len(out1) > 0:
			if out1[-1] == 0 or len(out1) >= maxLen:
				if out1[-1] == 0:
					out1 = out1[:-1]
				break

		temp = pad_right(np.array(out1, dtype=np.float32), maxLen)

		modelInput = np.concatenate((np.array([]), temp, temp2))

		for i in model.predict(modelInput.reshape(1, 400)):
			out1.append(find_dominant_neuron(i)[0])
			out2.append(find_dominant_neuron(i)[1])

		#print ('.')

	return arr_to_vocab(out1, vocabTo), out1, out2