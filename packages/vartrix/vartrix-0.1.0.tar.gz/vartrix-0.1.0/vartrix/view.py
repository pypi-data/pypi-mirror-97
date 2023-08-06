# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 20:59:39 2019

@author: Reuben

View instances make it easier to interact with containers. For example, 
if a container includes keys 'A.a' and 'A.b', we could make a view for all
keys beginning with 'A'. The view would then have keys 'a', and 'b', because
those are subkeys of 'A'.

"""

import uuid
from contextlib import contextmanager

from . import utils
from . import settings

def get_bases(obj):
    ''' Get a list of bases for an object instance '''
    def dotkey(c):
        long_name = c.__module__ + '.' + c.__name__
        split = long_name.split('.')
        return '.'.join(split[1:])
        
    bases = [dotkey(obj.__class__)]
    for base_class in obj.__class__.__bases__:
        bases.append(dotkey(base_class))
    if 'object' in bases:
        bases.remove('object')
    return bases


class View(dict):
    ''' Provides a virtual view of a Container
    
    Args:
        container (Container): The container
        dotkeys (list[str]): A list of strings specifying the dotkey prefixes
        for the view.
        live (bool): Optional boolean to specify whether the view stays in
        sync with the container. Defaults to settings.LIVE_VIEWS.
        obj (object): Instead of specifying dotkeys, an object can be passed
        in. The bases of the object will be used as dotkeys (after removing
        the top-level key).
        
    Note:
        Views cache values and update them as required for performance. They
        provide both dictionary-style access and attribute-style access to
        values.
        
    Note:
        Subdictionaries are updated from the container. But, any values
        set in subdictionaries on the View do not update those in the
        container.
        
    '''
    def __init__(self, container, dotkeys=None, live=None,
                 obj=None, nesting=True, numpify=None):
        self.__hash = hash(uuid.uuid4())
        self._container = container
        self.dotkeys = []
        self._live = settings.LIVE_VIEWS if live is None else live
        self.dirty = False
        self.nesting = nesting
        self.numpify = numpify
        dotkeys = ['__ROOT__'] if dotkeys is None else dotkeys
        dotkeys = [dotkeys] if isinstance(dotkeys, str) else dotkeys
        dotkeys = get_bases(obj) if obj is not None else dotkeys
        for dotkey in dotkeys:
            self.add_dotkey(dotkey)
    
    @property
    def live(self):
        return self._live
    
    @live.setter
    def live(self, flag):
        assert type(flag) is bool
        self._live = flag
        if self._live:
            self.refresh()
        
    def __hash__(self):
        return self.__hash
        
    def add_dotkey(self, dotkey):
        if dotkey is None or dotkey in ['', '.']:
            dotkey == '__ROOT__'
        self._hook_to_container(dotkey)
    
    def _clash_error(self, key, dotkey):
        raise KeyError('Key "' + str(key) + '" defined in '
                       + dotkey + ' when already present in '
                       + 'one of: "' + '"; "'.join(self.dotkeys) + '"')
        
    def _hook_to_container(self, dotkey):
        self._container.register_observer(dotkey, self)
        self._update(dotkey)
        self.dotkeys.append(dotkey)
        
    def _update(self, dotkey):
        try:
            dct = utils.nested(self._container.get_dct(dotkey))
        except KeyError:
            return
        for key in dct.keys():
            if key in self:
                self._clash_error(key, dotkey)
        for k, v in dct.items():
            self._set_val(k, v)
        
    def refresh(self):
        ''' Refresh all values if required '''
        if not self._live:
            return
        old_keys = self.keys()
        self.clear()
        for dotkey in self.dotkeys:
            self._update(dotkey)
        new_keys = self.keys()
        for old_key in old_keys:
            if old_key not in new_keys:
                delattr(self, old_key)
        self.dirty = False

    def check_refresh(self):
        ''' Refresh if current values only if they are indicated as dirty '''
        if self.dirty:
            self.refresh()
        
    def get(self, key, *args):
        ''' Get a value '''
        return dict.get(self, key, *args)
        
    def set(self, key, val):
        ''' Set a value 
        
        Note:
            If `live` is true, this method will also set the value in the
            container. The key must already exist.
        '''
        if not self._live:
            self._set_val(key, val)
            return
        container = self._container
        for dotkey in self.dotkeys:
            k = dotkey + '.' + key
            if k in container:
                container.set(k, val)
                return
        raise KeyError(key + ' not found in dotkeys: ' + '; '.join(self.dotkeys))
        
    def __setitem__(self, key, val):
        return self.set(key, val)
    
    def _nested_set(self, key_list, val, dct=None):
        d = self if dct is None else dct
        if len(key_list) > 1:
            root = key_list[0]
            if root not in d:
                d[root] = {}
                setattr(self, root, d[root])
            d_sub = d[root]
            self._nested_set(key_list[1:], val, dct=d_sub)
        else:
            key = key_list[0]
            if d is self:
                self._set_val(key, val)
            else:
                d[key] = val
    
    def _view_update(self, key, val):
        if self._live:
            self._nested_set(key.split('.'), val)
    
    def _set_val(self, key, val):
        if (self.numpify is not None 
            and (self.numpify is True or key in self.numpify)):
                val = utils.numpify(val)
        super().__setitem__(key, val)
        setattr(self, key, val)
    
    def dset(self, dct):
        ''' Set multiple values using a dictionary '''
        for k, v in dct.items():
            self.set(k, v)
            
    @contextmanager
    def context(self, dct):
        ''' A context manager for temporary changes in values 
        
        Args:
            dct (dict): A dictionary of dotkey-value pairs.
        '''
        originals = {k: self[k] for k in dct.keys()}
        self.dset(dct)
        yield self
        self.dset(originals)