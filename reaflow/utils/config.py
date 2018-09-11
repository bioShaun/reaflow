#!/usr/bin/env python3

''' reaflow config file
'''

import inspect
import pkg_resources
from configparser import ConfigParser, ExtendedInterpolation
#from . import tools
import tools
from reaflow.data import TEST_CFG
import doctest


# load expression base functions
base_func = dict()
for entry_point in pkg_resources.iter_entry_points('ExpBase'):
    base_func.update({entry_point.name: entry_point.load()})


class FlowParams:
    '''
    Extract function params from config

    test fromfile
    >>> test_param_obj = FlowParams.fromfile(TEST_CFG)
    >>> test_param_obj._cfg_dict == {}
    True
    >>> cfg_obj = ConfigParser(interpolation=ExtendedInterpolation())
    >>> cfg_obj.read(TEST_CFG)
    ['/public/scripts/reaflow/reaflow/data/test.cfg']
    >>> test_param_obj.cfg_obj == cfg_obj
    True

    test params
    >>> def test_func(gene_type, exp_cutoff):
    ...     pass
    >>> param_dict = test_param_obj.params(test_func, label='test_func')
    >>> param_dict == {'gene_type': 'protein_coding',
    ... 'exp_cutoff': '0.1',
    ... '_func_label': 'test_func'}
    True
    >>> test_param_obj._cfg_dict == {'gene_type': 'protein_coding',
    ... 'exp_cutoff': '0.1'}
    True
    '''

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


def FlowFuncs(func_dict=base_func, **kwargs):
    '''
    Wrapper for functions used in airflow

    prepare test file
    >>> valid_file = pathlib.Path(__file__)
    >>> valid_file = valid_file.resolve()
    >>> invalid_file = valid_file.with_suffix('.invalid')

    normal situation: input is valid and output not exists
    >>> params = {'params':
    ...                   {'test_input': valid_file
    ...                    'test_output': invalid_file}}
    >>> def test_func(test_input, test_output):
    ...     """
    ...     input: test_input
    ...     output: test_output
    ...     """
    ...     pass
    >>> FlowFuncs()
    '''
    params_dict = kwargs['params'].copy()
    func_name = params_dict.pop('_func_label')
    func = base_func[func_name]
    if tools.check_in_out(func, params_dict):
        return f'{func_name} is done.'
    else:
        return func(**params_dict)
