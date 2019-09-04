# lose.py

`LOSE()` is a helper class for handling data using `hdf5` file format and `tables` lib

## structure
#### vars
`LOSE.fname` is the path to  to the `.h5` file including the name and extension, default is `None`.

`LOSE.fmode` is the mode `.h5` file from `LOSE.fname` will be opened with, `'r'` for read(default), `'w'` for write, `'a'` for append.

`LOSE.atom` recommended to be left at default, is the `dtype` for the data to be stored in, default is `tables.Float32Atom()` which results to arrays with `dtype==np.float32`.

`LOSE.batch_obj` default is `'[:]'`, recommended to be left default, specifies the amount of data to be loaded by `LOSE.load()`, works like python list slicing, must be a string, default loads everything.

**`LOSE.generator()` related vars:**

`LOSE.batch_size` batch size of data getting pulled from the `.h5` file, default is 1.

`LOSE.loopforever` bool that allows infinite looping over the data, default is `False`.

`LOSE.iterItems` list of X group names and list of Y group names, default is `None`, required to be user defined for `LOSE.generator()` to work.

`LOSE.iterOutput` list of X output names and list of Y output names, default is `None`, required to be user defined for `LOSE.generator()` to work.

#### methods
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


`LOSE.save(**groupNamesAndSahpes)` is used to save data in write/append mode(depends on the file mode) into a group into a `.h5` file, the data needs to have the same shape as `group.shape[1:]` the data was passed to, `LOSE.get_shape(groupName)` can be used to get the `group.shape` of a group.


`LOSE.load(*groupNames)` is used to load data(hole group or a slice, to load a slice change `LOSE.batch_obj` to a string with the desired slice, default is `"[:]"`) from a group, group has to be present in the `.h5` file.


`LOSE.get_shape(groupName)` is used to get the shape of a single group, group has to be present in the `.h5` file.


`LOSE.generator()` is an python generator obj used to iterate through data, `LOSE.iterItems` and `LOSE.iterOutput` have to be defined for it to work, more info on how they should be defined checkout `LOSE.generator() details`.

## example usage

##### creating new groups in append/write mode 
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file, has to be user defined before any methods can be used, default is None
l.fmode = 'w' # 'w' for write mode, 'a' for append mode, default is 'r'

exampleDataX = np.arange(20, dtype=np.float32)
exampleDataY = np.arange(3, dtype=np.float32)

l.newGroup(x=(0, *exampleDataX.shape), y=(0, *exampleDataY.shape)) # creating new groups(ready for data saved to) in a file, if fmode is 'w' all groups in the file will be overwritten 
```
##### saving data into a group in append/write mode
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file, has to be user defined before any methods can be used, default is None
l.fmode = 'a' # 'w' for write mode, 'a' for append mode, default is 'r', 'a' mode append data to the file, 'w' mode overwrites data for the group in the file

exampleDataX = np.arange(20, dtype=np.float32)
exampleDataY = np.arange(3, dtype=np.float32)

l.save(x=[exampleDataX, exampleDataX], y=[exampleDataY, exampleDataY]) # saving data into groups defined in the previous example, in append mode
l.save(y=[exampleDataY], x=[exampleDataX]) # the same thing
```
##### loading data from a file
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file, has to be user defined before any methods can be used, default is None

x, y = l.load('x', 'y')				 # loading data from the .h5 file(has to be a real file) populated by previous examples
y2compare, x2compare = l.load('y', 'x') # the same thing 

print (np.all(x == x2compare), np.all(y == y2compare)) # True True
```
##### getting the shape of a group
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to the .h5 file(populated by previous examples), has to be user defined before any methods can be used, default is None

print (l.get_shape('x')) # (3, 20)
print (l.get_shape('y')) # (3, 3)
```
## `LOSE.generator()` details
`LOSE.generator()` is a python generator used to access data from a `.h5` file in `LOSE.batch_size` pieces without loading the hole file or the hole group into memory, also works with `model.fit_generator()`.

`LOSE.iterItems` and `LOSE.iterOutput` __have__ to be defined by user first

### example `LOSE.generator()` usage
for this example let's say that file has requested data in it
```python
import numpy as np
from lose import LOSE

l = LOSE()
l.fname = 'path/to/you/save/file.h5' # path to data

l.iterItems = [['x1', 'x2'], ['y']] # names of X groups and names of Y groups, all group names need to have most outer dim the same and be present in the .h5 file
l.iterOutput = [['input_1', 'input_2'], ['dense_5']] # names of model's layers the data will be cast on, group.shape[1:] needs to match the layer's input shape
l.loopforever = True
l.batch_size = 20 # some batch size, can be bigger then the dataset, but won't output more data, it will just loop over or stop the iteration if LOSE.loopforever is False

some_mode.fit_generator(l.generator(), steps_per_epoch=50, epochs=1000, shuffle=False) # the only down side is that it can't be shuffled by model.fit_generator(), yet...
```