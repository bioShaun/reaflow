#!/usr/bin/env python3

''' reaflow config file
'''

import inspect
import pkg_resources
from configparser import ConfigParser, ExtendedInterpolation


# load expression base functions
base_func = dict()
for entry_point in pkg_resources.iter_entry_points('ExpBase'):
    base_func.update({entry_point.name: entry_point.load()})


# extract function params from config
class FlowParams:

    def __init__(self, cfg_obj, cfg_dict=None):
        self.cfg_obj = cfg_obj
        if cfg_dict is None:
            self._cfg_dict = {}
        else:
            self._cfg_dict = cfg_dict

    @property
    def cfg_dict(self):
        if self._cfg_dict:
            return self._cfg_dict
        for section in self.cfg_obj.sections():
            for key in self.cfg_obj[section]:
                self._cfg_dict.update(
                    {key: self.cfg_obj[section][key]})
        return self._cfg_dict

    def params(self, func, label=None):
        param_dict = {}
        sig = inspect.signature(func)
        for each in sig.parameters:
            if each in self.cfg_dict:
                param_dict.update({each: self.cfg_dict[each]})
            else:
                if sig.parameters[each].default is inspect._empty:
                    raise KeyError(f'Can not find [{each}] in configfile.')
                else:
                    param_dict.update({each: sig.parameters[each].default})
        if label is not None:
            param_dict.update({'_func_label': label})
        return param_dict

    @classmethod
    def fromfile(cls, cfg_file):
        cfg_obj = ConfigParser(interpolation=ExtendedInterpolation())
        cfg_obj.read(cfg_file)
        return cls(cfg_obj)


def FlowFuncs(**kwargs):
    params_dict = kwargs['params'].copy()
    func_name = params_dict.pop('_func_label')
    return base_func[func_name](**params_dict)
