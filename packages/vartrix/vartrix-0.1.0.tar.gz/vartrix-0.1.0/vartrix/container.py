# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 19:52:22 2019

@author: Reuben

This module includes the Container class upon which all of vartrix is built.

The idea of a container is to contain all of the key-value pairs for some
set of variables or parameters. Keys have an implied heirarchy using a
dot-format. For example, 'A.b' means that 'b' is a subkey of 'A'. All keys
are stored in a simple flat dictionary format, but some extra methods
allow the heirarchy to be used to simplify usage.

"""

import weakref
from collections import defaultdict
from contextlib import contextmanager

from . import utils

def is_root(dotkey):
    ''' Check if a dotkey is the root (container level) '''
    return dotkey in [None, '__ROOT__', '', '.']

def safe_root(dotkey):
    ''' Ensure root dotkeys are consistent '''
    if is_root(dotkey):
        return '__ROOT__'
    else:
        return dotkey


class Picker():
    def __init__(self, container, dotkey):
        self._container = container
        self._dotkey = dotkey
        
    def __getattr__(self, key):
        return self._container[self._dotkey + '.' + key]

    def __getitem__(self, key):
        return self._container[self._dotkey + '.' + key]


class Container(dict):
    ''' A dictionary-like class that updates observers 
    
    Args:
        dct (dict): A dictionary (possibly nested) of key-value pairs to use.
        name (str): The name of the container.
        
    Note:
        A `dotkey` is a dictionary key in the Container. It's called a dotkey
        simply because it's designed to have dots in it to represent a
        heirarchy.
    '''

    def __init__(self, dct=None, name=None):
        self.name = name
        self._observers = defaultdict(weakref.WeakSet)
        self._backup = {}
        if dct is not None:
            self.load(dct)

    def get(self, dotkey):
        ''' Return the value of a dotkey '''
        return self[dotkey]

    def lget(self, key_list):
        ''' Return the value of a dotkey specified by a list of strings
        
        Args:
            key_list (list([str])): The strings that define the dotkey. For
            example, `['a', 'b']` would equate to the dotkey `'a.b'`.
        '''
        return self['.'.join(key_list)]

    def dget(self, dotkeys):
        ''' Return a dictionary of dotkey-values for multiple dotkeys 
        
        Args:
            dotkeys (list[(str)]): A list of dotkey strings.
        '''
        dct = {}
        for dotkey in dotkeys:
            dct[dotkey] = self[dotkey]
        return dct
            
    def set(self, dotkey, val, safe=False):
        ''' Set the value of a dotkey 
        
        Args:
            dotkey (str): The key value
            val: The value to set. It can be a numpy array.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        if safe and dotkey not in self:
            raise KeyError('In safe mode, key ' + dotkey + ' must be present.')
        v = utils.denumpify(val)
        super().__setitem__(dotkey, v)
        self.update_observers(dotkey, v)
        
    def lset(self, key_list, val, safe=False):
        ''' Set the value of a dotkey specified as a list 
        
        Args:
            dotkey (list([str])): The list of strings for the dotkey.
            val: The value to set. It can be a numpy array.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        self.set('.'.join(key_list), val)

    def dset(self, dct, safe=False):
        ''' Set multiple values specified in a dictionary
        
        Args:
            dct (dict): The dictionary of dotkey-value pairs.
            safe (bool): Optional boolean. If true, the dotkey must already
            exist in the Container instance.
        '''
        for dotkey, val in dct.items():
            self.set(dotkey, val, safe=safe)

    def register_observer(self, dotkey, view):
        ''' Register an observer (typically a view) for a dotkey prefix
        
        Args:
            dotkey (str): The associated dotkey prefix
            view (View): A view instance (or other compatible object)
            
        Note:
            Here, the dotkey is for a higher level of the heirarchy. For
            example, if the container includes dotkeys of 'a.b.a', 'a.b.b', and
            'a.b.c', the dotkey specified here could be 'a.b'. It would 
            then ensure the view got data for all dotkeys beginning with 
            'a.b' (e.g. 'a.b.c'). Nested dotkeys are not included. 
            E.g. 'a.b' would not capture the dotkey of 'a.b.c.d'.
        '''
        self._observers[safe_root(dotkey)].add(view)

    def __contains__(self, key):
        found = super().__contains__(key)
        if found:
            return True
        if is_root(key):
            return False
        try:
            dct = self.get_dct(key)
            return True
        except KeyError:
            return False

    def __missing__(self, key):
        try:
            ret = self.get_dct(key)
        except:
            raise KeyError("Key '" + str(key) + "' not found. Check aliases.")
        return ret

    def get_dct(self, dotkey):
        ''' Return a dictionary of all key-value pairs for a dotkey prefix 
        
        Args:
            dotkey (str): The dotkey prefix. The dictionary will include all
            dotkeys that begin with this prefix.
            
        Note:
            Changes within nested dictionaries are not tracked.
        '''
        if is_root(dotkey):
            return self.copy()
        out = {}
        s = dotkey + '.'  # Force it to be a dot
        n = len(s)
        for key, val in self.items():
            if key.startswith(s):
                out[key[n:]] = val
        if len(out) == 0:
            raise KeyError("'" + dotkey + "'")
        return out

    def update_observers(self, dotkey, val):
        ''' Update the observers for a given dotkey with a value '''
        def all_possible(dotkey):
            ''' Include observes at higher levels '''
            split = dotkey.split('.')
            roots = ['__ROOT__']
            keys = [dotkey]
            for i in range(1, len(split)):
                roots.append('.'.join(split[:i]))
                keys.append('.'.join(split[i:]))
            return roots, keys
        for root, key in zip(*all_possible(dotkey)):
            for view in self._observers[root]:
                view._view_update(key, val)

    def __setitem__(self, key, val):
        return self.set(key, val)
    
    def _split_dotkey(self, dotkey):
        ''' Split a string dotkey into its root (prefix) and key '''
        split = dotkey.split('.')
        k = split.pop()
        root = safe_root('.'.join(split))
        return root, k

    def nested(self):
        ''' Create a nested dictionary representation of the container '''
        return utils.nested(self)
    
    def container(self, dct, parents=None, current=None):
        ''' Create a container dictionary (recursively) 
        
        Note:
            This method uses recursion to handle nested dictionaries.
        '''
        current = {} if current is None else current
        parents = [] if parents is None else parents
        for key, obj in dct.items():
            full_key = parents + [str(key)]
            if isinstance(obj, dict):
                self.container(obj, parents=full_key, current=current)
            else:
                current['.'.join(full_key)] = obj
        return current
    
    def load(self, dct):
        ''' Set the container data using a dictionary '''
        self.clear()
        self._backup.clear()
        self.add(dct)
        
    def reset(self):
        self.load(self._backup.copy())
        
    def add(self, dct):
        ''' Add another set of data to the container '''
        cdct = self.container(dct)
        self.update(cdct)
        self._backup.update(cdct)
        for dotkey, observers in self._observers.items():
            for observer in observers:
                observer.dirty = True
        for dotkey, observers in self._observers.items():
            for observer in observers:
                observer.check_refresh()
                
    @classmethod
    def combine(cls, dct):
        ''' Combine a dictionary of containers '''
        c = cls()
        for key, container in dct.items():
            for k, v in container.items():
                dotkey = key + '.' + k
                c[dotkey] = v
        return c
    
    @classmethod
    def merge(cls, containers):
        ''' Combine a dictionary of containers '''
        c = cls()
        for container in containers:
            c.update(container)
            for dotkey, observers in container._observers.items():
                c._observers[dotkey] |= observers # set union, in place
        return c
    
    @contextmanager
    def context(self, dct, safe=True):
        ''' A context manager for temporary changes in values 
        
        Args:
            dct (dict): A dictionary of dotkey-value pairs.
        '''
        originals = {k: self[k] for k in dct.keys()}
        self.dset(dct, safe=safe)
        yield self
        self.dset(originals, safe=safe)
        
    def get_picker(self, dotkey):
        return Picker(self, dotkey)
    
    def copy(self):
        return Container(dct=self, name=self.name)
    
    def to_dict(self):
        return dict(self)