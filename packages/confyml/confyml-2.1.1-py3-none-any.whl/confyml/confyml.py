import logging
import os
import traceback
from functools import wraps
from typing import List, Tuple, Set, Dict

import yaml


logger = logging.getLogger(__name__)


class Config:

    def __init__(self, yaml_file: str, mode: str = None) -> None:
        """
        Instantiate the Config class

        Parameters
        ----------
        yaml_file : str
            File path to yaml config file
        mode : str
            Mode that config is being applied
              'mcf' : modules and classes and methods and/or modules .
                      and functions
              'mf' : modules and functions only.
              'cf' : classes and methods and/or functions.
              'f' : functions only.
        """
        self._path = yaml_file
        self._mode_name = mode
        mode_map = {'mcf': 3, 'mf': 2, 'cf': 2, 'f': 1}
        self._mode = mode_map[mode]
        self._config = {}
        if yaml_file:
            with open(yaml_file, 'r') as f:
                self._config = yaml.safe_load(f)

        self._configured = self._get_objects()

    @property
    def mode(self) -> int:
        return self._mode

    def __getitem__(self, item: str):
        return self._config[item]

    def _get_objects(self) -> List[Set]:
        """
        Gets a list of all functions and classes that have been
        configured in the yaml config.

        Returns
        -------
        set
            Set of object names that are configured in the yaml.
        """
        named = (None, self._config.copy())

        out, log = _reduce([named])

        for i in range(self.mode):
            out, log = _reduce(out, log)
        return list(set(log))

    def _get_config(self, name) -> Dict:
        conf = self._config.copy()
        key_list = name.split('.')
        for k in key_list:
            conf = conf[k]
        return {k: v for k, v in conf.items() if not isinstance(v, dict)}

    def apply(self, func: object) -> object:
        """Apply the config to the function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            name_map = {'f': func.__name__,
                        'mf': f'{func.__module__.split(".")[-1]}'
                              f'.{func.__name__}',
                        'cf': func.__qualname__,
                        'mcf': f'{func.__module__.split(".")[-1]}'
                               f'.{func.__qualname__}'}

            name = name_map[self._mode_name]
            if '.__init__' in name:
                name = name.replace('.__init__', '')
            return self._wrap(name, func, *args, **kwargs)
        return wrapper

    def _wrap(self, name, func, *args, **kwargs):
        if name not in self._configured:
            return func(*args, **kwargs)

        func_to_replace = [fn for fn in self._configured if fn == name]

        if len(func_to_replace) > 1:
            raise ReferenceError(f'Multiple definitions for function {name}')

        conf = self._get_config(func_to_replace[0])
        conf.update(**kwargs)
        logger.info(f'Applying config to {func.__qualname__}')
        return func(*args, **conf)


def _reduce(ds: List[Tuple], store: List = None) -> Tuple[List[Tuple], List]:
    """
    Returns list of tuples and list of key names associated. Not
    to be used directly.
    """
    # Store to hold the parent key names
    if store is None:
        store = []

    # Loop through _NamedDicts in the list
    dicts = []
    for d in ds:
        for k, v in d[1].items():
            if isinstance(v, dict):

                # If item is a dict itself, create a _NamedDict and
                # add to the name with the key of that dict.
                new_name = d[0] + '.' + k if d[0] else k
                inner_d = (new_name, v)

                dicts.append(inner_d)

            elif not isinstance(v, dict):
                # If the value is a string, not a dict, this is the
                # level the kwargs are set
                store.append(d[0])

    return dicts, store


def set_config(yaml_path, mode=None):
    if not mode:
        raise AttributeError('Mode not provided to confyml.set_config.')
    stack = traceback.extract_stack()
    caller = os.path.dirname(stack[-2].filename)
    full_path = os.path.realpath(os.path.join(caller, yaml_path))

    os.environ['CONFYML_CONFIG'] = str(full_path)
    os.environ['CONFYML_MODE'] = str(mode)

    try:
        get_config()
    except FileNotFoundError as e:
        del os.environ['CONFYML_CONFIG']
        del os.environ['CONFYML_MODE']
        raise FileNotFoundError("Config YML not found")


def get_config():
    file = os.environ.get('CONFYML_CONFIG')
    mode = os.environ.get('CONFYML_MODE')

    if file is None:
        logger.warning("Confyml Config imported without config file set. Set "
                       "environment variable CONFYML_CONFIG to apply "
                       "config.", UserWarning, stacklevel=2)

    return Config(file, mode=mode)
