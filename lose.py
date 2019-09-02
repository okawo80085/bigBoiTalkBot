import numpy as np
import tables as t

class LOSE:
	def __init__(self):
		self.fname = None
		self.fmode = 'r'
		self.atom = t.Float32Atom()

		self.batch_size = 1

		self.iterItems = None
		self.iterOutput = None
		self.loopforever = False
		self.index = 0
		self.limit = None

		self.batch_obj = '[:]'

	def __repr__(self):
		if self.fname is None:
			return '<.h5 data handler, fname={}, fmode=\'{}\', atom={}>'.format(self.fname, self.fmode, self.atom)
		else:
			with t.open_file(self.fname, mode=self.fmode) as f:
				return '<.h5 data handler, fname={}, fmode=\'{}\', atom={}>\n\n.h5 file structure: {}'.format(self.fname, self.fmode, self.atom, f)

	def newGroup(self, **kwards):
		with t.open_file(self.fname, mode=self.fmode) as f:
			for key, val in kwards.items():
				f.create_earray(f.root, key, self.atom, val)
				print ([key], val)

			print (f)

	def save(self, **kwards):
		with t.open_file(self.fname, mode=self.fmode) as f:
			for key, val in kwards.items():
				x = eval('f.root.{}'.format(key))
				x.append(val)

	def load(self, *args):
		out = []
		with t.open_file(self.fname, mode=self.fmode) as f:
			for key in args:
				x = eval('f.root.{}{}'.format(key, self.batch_obj))
				out.append(x)

		return out

	def generator(self):
		if self.iterItems is None or self.iterOutput is None or self.fname is None:
			raise ValueError('self.iterItems and/or self.iterOutput and/or self.fname is empty')

		with t.open_file(self.fname, mode='r') as f:
			dataset_limit = eval('f.root.{}.shape[0]'.format(self.iterItems[0]))

		#print (dataset_limit)

		while 1:
			step = {}
			for name, key in zip(self.iterItems, self.iterOutput):
				with t.open_file(self.fname, mode='r') as f:
					x = eval('f.root.{}[{}:{}]'.format(name, self.index, self.index+self.batch_size))

					step[key] = x

			yield step

			self.index += self.batch_size

			if self.limit is not None:
				if self.index >= self.limit or self.index >= dataset_limit:
					self.index = 0

					if not self.loopforever:
						raise StopIteration

			elif self.index >= dataset_limit:
				self.index = 0
				if not self.loopforever:
					raise StopIteration