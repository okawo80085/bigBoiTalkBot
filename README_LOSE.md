# lose.py

`LOSE()` is a helper class for handling data using `hdf5` file format

## structure of LOSE() class
```
Help on LOSE in module lose object:

class LOSE(builtins.object)
 |  Methods defined here:
 |  
 |  __init__(self)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __repr__(self)
 |      Return repr(self).
 |  
 |  generator(self)
 |  
 |  get_shape(self, groupName)
 |  
 |  load(self, *args)
 |  
 |  newGroup(self, **kwards)
 |  
 |  save(self, **kwards)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
```

`LOSE.newGroup(**groupNames)` is used to add/set(depends on the file mode) group(expandable array) names and shapes in the `.h5` file.


`LOSE.save(**groupNames)` is used to save data in write/append mode(depends on the file mode) into a group into a `.h5` file, the data needs to have the same shape as `group.shape[1:]` the data was passed to, `LOSE.get_shape(groupName)` can be used to get the `group.shape` of a group.


`LOSE.get_shape(groupName)` is used to get the shape of a group, group has to be present in the `.h5` file.


`LOSE.load(*groupNames)` is used to load data(hole group or a slice, to load a slice change `LOSE.batch_obj` to a string with the desired slice, default is `"[:]"`) from a group, group has to be present in the `.h5` file.


## examples

setting new group to a file:
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # default is None
l.fmode = 'w' 						 # default is 'r'

exampleData = np.arange(20, dtype=np.float32)

l.newGroup(arr1=(0, *exampleData.shape))
```