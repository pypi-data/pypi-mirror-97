"""
attrdict contains several mapping objects that allow access to their
keys as attributes.
"""
from lsattrdict.mapping import AttrMap
from lsattrdict.dictionary import AttrDict
from lsattrdict.default import AttrDefault


__all__ = ['AttrMap', 'AttrDict', 'AttrDefault']
