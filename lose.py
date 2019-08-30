import numpy as np
import tables as t

class LOSE:
	def __init__(self):
		self.fname = 'temp.h5'
		self.fmode = 'w'
		self.atom = t.Float32Atom()

	def newFile(self, **kwards):
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
'''
lose = LOSE()
lose.fname = 'test.h5'
lose.newFile(x1=(0, 10), x2=(0, 20))
lose.fmode = 'a'
lose.save(x2=[np.arange(0, 20)])
lose.save(x2=[np.arange(0, 20)])
lose.save(x1=[np.arange(0, 10)])
lose.fmode = 'r'
x, y = lose.load('x1', 'x2')
print (x, y)
'''