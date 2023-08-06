# vartrix

Vartrix is about managing and automating parameters used in code. The name 'vartrix' is short for 'variable tricks'.

You might like vartrix if:

* You're worried about the growing complexity of all the parameters in your code and you'd like to use a robust, scalable approach from the start.
* Tracking all the parameters in your code has become difficult.
* You need parameters to be traceable so you are confident that the right ones are used
* You need to change parameters in a simple, robust and traceable way to ensure you haven't got an undetected coding error.
* You need to be able to snapshot parameters and store them.
* You've created ugly, fragile code to step through sets of parameters and run bits of code for each set.
* You pass around a lot of parameters between classes in your code, making it bloated, difficult to maintain, and fragile


## Quickstart tutorial - basic usage

Install using:

```
pip install vartrix
```

Then in your code, import vartrix to get started:

```python
import vartrix
```

### Containers
A container is a dictionary-like object that contains a set of parameters. The keys are 'dotkeys'. For example, 'a.b.c', or 'subpackage.module.class.key'.

There are a few ways to set up containers. First, from a nested dictionary:
```python
dct = {'A': {'apple': 5, 'banana': 7, 'grape': 11},
	   'B': {'fig': 13, 'pear': 17, 'orange': 19}}
container = vartrix.Container(dct)
print(container)
# {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```

From a flat ('dotkey') dictionary:
```python
dct = {'A.apple': 5, 'A.banana': 7, 'A.grape': 11,
	   'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
container = vartrix.Container(dct)
print(container)
# {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```

You can use any dictionary to set up the Container.

### Name spaces

Usually, we set containers up using a Name_Space instance. You can use the default:
```python
container = vartrix.get_container('example_name')
```

Or, set up your own:
```python
ns = vartrix.Name_Space()
container = ns.create('example_name_2', dct=dct)
```

Initialise it with a dictionary, like the above, or load one into it. A short way to set up a container is like this, as new containers are created if required:
```python
ns['tutorial_1'].load(dct)
```


### Views
For large containers with multiple levels, it's much easier to deal with a View of a specific set of the dotkeys. Views allow the values for those dotkeys to be accessed without the preceeding levels of the key. For example:

```python
view_A = vartrix.View(ns['tutorial_1'], dotkeys='A')
print(view_A)
# {'apple': 5, 'banana': 7, 'grape': 11}
```

Views have both dictionary-style key access and attribute-style access:
```python
print(view_A['apple'])
# 5
print(view_A.apple)
# 5
```

You can use them in a class like this:
```python
class B():
	def __init__(self):
		self.params = vartrix.View(ns['tutorial_1'], dotkeys=['B'])

b = B()
print(b.params)
# {'fig': 13, 'pear': 17, 'orange': 19}
```

You can pass in the object instead. It will automatically remove the package name or `__main__` prefix on the class names. It automatically includes base classes so inheritance works.

```python
class A():
	def __init__(self):
		self.params = vartrix.View(ns['tutorial_1'], obj=self)
		# Class A objects have signature 'tutorial_1.A'
a = A()
print(a.params)
# {'apple': 5, 'banana': 7, 'grape': 11}
```
 
You can use multiple dotkeys:
```python
class Combined():
	def __init__(self):
		self.params = vartrix.View(ns['tutorial_1'], dotkeys=['A', 'B'])
c = Combined()
print(c.params)
# {'A.apple': 5, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```
	
	
### Remote updates
The views are automatically updated with changes from their associated container. Let's first make a view and get a reference to the container:

```python
a = A()
container = ns['tutorial_1']
```

Let's update the 'A.apple' value using setitem style:
```python
container['A.apple'] = 101
print(container['A.apple'])
# 101
print(a.params['apple'])
# 101
```

We can use the 'set' method:
```python
container.set('A.apple', 102)
print(container['A.apple'])
# 102
```python

Use the `lset` method for dotkets as lists of strings:
```python
container.lset(['A', 'apple'], 103)
print(container['A.apple'])
# 103
```

And use the `dset` method to set a range of values using a dictionary of dotkeys:
```python
{'A.apple': 103, 'A.banana': 7, 'A.grape': 11, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
container.dset({'A.apple': 104, 'A.grape': 201})
print(container)
{'A.apple': 104, 'A.banana': 7, 'A.grape': 201, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```

### Preventing updating
If you don't want a view to update, set the `live` attribute to False, like this:
```python
a.params.live = False
container.dset({'A.apple': 111, 'A.grape': 222})
print(container)
# {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
print(a.params)
# {'apple': 104, 'banana': 7, 'grape': 201}
```

Call the `refresh()` method to manually refresh non-live Views. They automatically refresh when they are set back to live:
```python
a.params.live = True
print(a.params)
# {'apple': 111, 'banana': 7, 'grape': 222}
```


Live views stay up to date with the container, even when keys are added or removed:
```python
backup = container.copy()
dct = {'A.apple': 77, 'A.banana': 87, 'A.grape': 91, 'A.pineapple': 55,
	   'B.fig': 102, 'B.pear': 150, 'B.orange': 300}
container.load(dct)
print(a.params)
# {'apple': 77, 'banana': 87, 'grape': 91, 'pineapple': 55}
container.load(backup)
print(a.params)
# {'apple': 111, 'banana': 7, 'grape': 222}
```

To only set values temporarily, use the context manager:
```python
print(container)
# {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
d = {'A.apple': 555, 'B.orange': -7}
with container.context(d):
	print(container)
	# {'A.apple': 555, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': -7}
print(container)
# {'A.apple': 111, 'A.banana': 7, 'A.grape': 222, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
```


### View updates
Sometimes, it's more convenient to set values on a view. This works in a similar way. Values set on a live view are reflected in the container, and all other linked views.

Use a setitem style:
```python
a.params['apple'] = 1001
print(container['A.apple'])
# 1001
print(a.params['apple'])
# 1001
```

The `set` method:
```python
a.params.set('apple', 1002)
print(container['A.apple'])
# 1002
print(a.params['apple'])
# 1002
```

Or the `dset` method for multiple key-value pairs:
```python
a.params.dset({'apple': 1003, 'grape': 2002})
print(container)
# {'A.apple': 1003, 'A.banana': 7, 'A.grape': 2002, 'B.fig': 13, 'B.pear': 17, 'B.orange': 19}
print(a.params)
# {'apple': 1003, 'banana': 7, 'grape': 2002}
```
	
Use the context manager to set values temporarily:
```python
print(a.params)
# {'apple': 1003, 'banana': 7, 'grape': 2002}
d2 = {'apple': 400, 'grape': 1000}
with a.params.context(d2):
	print(a.params)
	# {'apple': 400, 'banana': 7, 'grape': 1000}
print(a.params)
# {'apple': 1003, 'banana': 7, 'grape': 2002}
```

## Quickstart tutorial - automation

### Setup

Let's set up a function to make a very simple Container first:
```python
import vartrix

ns = vartrix.Name_Space()

def setup_container():
    dct = {'A': {'apple': 1},
           'B': {'orange': 2, 'fig': 3}}
    container = ns['tutorial_2']
    container.load(dct)
```

Let's run it and check it's worked:

```python
setup_container()
print(ns['tutorial_2'])
# {'A.apple': 1, 'B.orange': 2, 'B.fig': 3}
```

### Sequences
Now, let's create a a set of automation parameters. They need to be a nested dictionary structure. We'll use a Yaml file to set them up.

tutorial_2.yml
```yaml
set_1:
    aliases:
        alias_1: A.apple
        alias_2: B.orange
        alias_3: B.fig
    vectors:
        vec_1:
            alias_1: [5, 10, 15]
        vec_2:
            labels:  ['a', 'b', 'c']
            alias_2: [  2,   3,   4]
            alias_3: [  6,   7,   8]
    sequences:
        seq_1:
            method_a: [vec_1, vec_2]
```

There are some key things about the structure:

* The highest level is for each set. Only one set is run at a time. Each `set` is labeled by its its key. In this case, we have one set called `set_1`.
* Each set needs three keys:
    * **aliases:** A dictionary where keys are aliases - shorter names for possibly long entries in the container - and the values are the corresponding container keys. The values need to exist as keys in the container.
	* **vectors:** Dictionary where each key-value pair specifies a series of values. The aliases must exist in the `aliases` dictionary. There are multiple formats, as described below.
	* **sequences:** A dictionary where each key is the name of a sequence. Inside each sequence, there are keys that correspond to method names in the class that we're going to use for the automation. The values are lists of vector names that must exist in the `vectors` dictionary. The way they work is described below.
	
#### How sequences work
Inside each sequence is a list of methods (the keys) and their corresponding list of vector names. The automator takes the list of vector names and interates over their values in a nested fashion. For example, `[vec_1, vec_2]` means the outer loop iterates over the set of values in `vec_1`, while the inner loop iterates over the values in `vec_2`. There is no limit to how many vectors you use, but since the total number of steps in the overall sequence grows exponentially, don't use too many.

#### Vectors
Vectors specify what values to iterate over for one or more aliases. There are many ways to specify them, as described below.

**Simple vector.** Labels of [0, 1, 2] will be automatically created. The `style` key-value pair is optional for this style.
```yaml
        vec_1:
            style: value_lists
            alias_1: [5, 10, 15]
```

**Value lists.** Here, we'll specify the labels in a separate vector. On the first iteration, the first values of each vector will be used. The second iteration will use the second values, and so on. The `style` key-value pair is optional for this style.
```yaml
        vec_2:
            style: value_lists
            labels:  ['a', 'b', 'c']
            alias_2: [  2,   3,   4]
            alias_3: [  6,   7,   8]
```

**Value dictionaries.** We could achieve the same `vec_2` as above using the format below:
```yaml
        vec_2:
            style: value_dictionaries
            a:  {alias_2: 2, alias_3: 6},
            b:  {alias_2: 3, alias_3: 7},
            c:  {alias_2: 4, alias_3: 8},
```

**Csv file.** We could achieve the same `vec_2` as above using a csv file combined with the format below. The filename is joined with the path at `vartrix.automate.root`, which can be set by calling `vartrix.automate.set_root(path)`.
```yaml
        vec_2:
            style: csv
            filename: tutorial_2.csv
```

tutorial_2.csv:

index | alias_2 | alias_3
----- | ------- | -------
'a' | 2 | 6
'b' | 3 | 7
'c' | 4 | 8


**Custom.** You can even use your own vector interpreter. Here's how:
* Inherit `vartrix.automate.Vector` and define a method called `setup`. It needs to accept one argument - a dictionary of data that excludes the `style` key-value pair. It needs to return a list of labels (strings), and a list of dictionaries that contain key-value pairs for the aliases and thier corresponding values (e.g. `[{'alias_1': 4, 'alias_2': 5}, {'alias_1': 8, 'alias_2': 9}]`).
* Add your style, by calling `vartrix.automate.Vector_Factor.set_style(style_name, vec_cls)`. The *style_name* is a string you specify. The *vec_cls* is the class you just created.
* Use *style_name* as the `style` value for any vectors that use your new style.
 


#### Initialisation

To initialise, just pass in a Container instance and the filename to load from:

```python
import os
root = os.path.dirname(__file__)
fname = os.path.join(root, 'tutorial_2.yml')
automator = vartrix.Automator(ns['tutorial_2'], fname)
```

### Automated classes

The vartrix Automator calls the method(s) specified in each sequence at each iteration through the nested vector loops. In addition, there are several methods that provide hooks:

* prepare(): Called at the start of the set
* prepare_sequence(seq_name): Called at the start of each sequence
* prepare_method(method_name): Called before starting to call `method_name` at each iteration
* method_name(seq_name, val_dct, label_dct): The only required method - the name must match that in the sequence dictionary.
* finish_method(method_name): Called after after calling `method_name` at each iteration
* finish_sequence(seq_name): Called at the end of each sequence
* finish(): Called at the end of the set

For this tutorial, we'll create a simple automated class like this:

```python
class Automated():
    def __init__(self):
        self.params = vartrix.View(ns['tutorial_2'], dotkeys=['A', 'B'])
        
    def prepare(self):
        print('preparing...')

    def prepare_sequence(self, seq_name):
        print('running sequence: ' + seq_name)

    def prepare_method(self, method_name):
        print('running method: ' + method_name)

    def method_a(self, seq_name, val_dct, label_dct):
        print('calling method_a:')
        print('current labels: ' + str(label_dct))
        print('current params: ' + str(self.params))

    def finish_method(self, method_name):
        print('finishing method: ' + method_name)

    def finish_sequence(self, seq_name):
        print('finishing sequence: ' + seq_name)

    def finish(self):
        self.finish = True
```

### Execution

Now for the easy part. We can simply create an instance of our Automated class and pass it into the automator with the set name.

```python
automated = Automated()
automator.run('set_1', automated)
```

The output looks like this:
```python
preparing...
running sequence: seq_1
running method: method_a
calling method_a:
current labels: {'vec_1': 0, 'vec_2': 'a'}
current params: {'apple': 5, 'orange': 2, 'fig': 6}
calling method_a:
current labels: {'vec_1': 0, 'vec_2': 'b'}
current params: {'apple': 5, 'orange': 3, 'fig': 7}
calling method_a:
current labels: {'vec_1': 0, 'vec_2': 'c'}
current params: {'apple': 5, 'orange': 4, 'fig': 8}
calling method_a:
current labels: {'vec_1': 1, 'vec_2': 'a'}
current params: {'apple': 10, 'orange': 2, 'fig': 6}
calling method_a:
current labels: {'vec_1': 1, 'vec_2': 'b'}
current params: {'apple': 10, 'orange': 3, 'fig': 7}
calling method_a:
current labels: {'vec_1': 1, 'vec_2': 'c'}
current params: {'apple': 10, 'orange': 4, 'fig': 8}
calling method_a:
current labels: {'vec_1': 2, 'vec_2': 'a'}
current params: {'apple': 15, 'orange': 2, 'fig': 6}
calling method_a:
current labels: {'vec_1': 2, 'vec_2': 'b'}
current params: {'apple': 15, 'orange': 3, 'fig': 7}
calling method_a:
current labels: {'vec_1': 2, 'vec_2': 'c'}
current params: {'apple': 15, 'orange': 4, 'fig': 8}
finishing method: method_a
finishing sequence: seq_1
```

The values in the Container are changed automatically by the Automator before calling `method_a`. But, the automator also passes in `val_dct`, a dictionary of automated key-value pairs, in case they are convenient. It's also often desirable to have shorter, simpler labels at each iteration for each vector, and the automator passes in `label_dct` for that purpose as well.

If we want to change the way we automate the parameters, now we only need to change the specification in our yaml file (`tutorial_2.yml`) - there's no need for manual coding of the automation. This approach has a number of advantages:

* Faster creation of iterative sequences
* Fewer mistakes
* Easier management of parameters
* Full traceability of how parameters are changed
* Flexble, loosely coupled code. The classes that use the values in the Container need no knowledge of the automation, and the automation needs no knowledge of them.


## Related packages

Other packages exist that overlap with vartrix in functionality. You might want to look at:

* parameters
* param
* paranormal
* traits
* traitlets
* attrs
* pypet