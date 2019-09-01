import numpy as np
import tables as t

class LOSE:
	def __init__(self):
		self.fname = None
		self.fmode = 'r'
		self.atom = t.Float32Atom()

	def __repr__(self):
		if self.fname is None:
			return '<.h5 data handler, fname={}, fmode={}, atom={}>'.format(self.fname, self.fmode, self.atom)
		else:
			with t.open_file(self.fname, mode=self.fmode) as f:
				return '<.h5 data handler, fname={}, fmode={}, atom={}>\n\n.h5 file structure: {}'.format(self.fname, self.fmode, self.atom, f)

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
				x = eval('f.root.{}[:]'.format(key))
				out.append(x)

		return out