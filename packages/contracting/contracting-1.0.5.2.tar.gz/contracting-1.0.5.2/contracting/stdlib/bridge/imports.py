import importlib
from types import FunctionType, ModuleType
from contracting.config import PRIVATE_METHOD_PREFIX
from contracting.db.orm import Datum
from contracting.db.driver import ContractDriver, OWNER_KEY
from contracting.execution.runtime import rt
from stdlib_list import stdlib_list
import sys

def extract_closure(fn):
    closure = fn.__closure__[0]
    return closure.cell_contents


class Func:
    def __init__(self, name, args=(), private=False):
        self.name = name

        if private:
            self.name = PRIVATE_METHOD_PREFIX + self.name

        self.args = args

    def is_of(self, f: FunctionType):

        if f.__closure__ is not None:
            f = extract_closure(f)

        num_args = f.__code__.co_argcount

        if f.__code__.co_name == self.name and f.__code__.co_varnames[:num_args] == self.args:
            return True
        return False


class Var:
    def __init__(self, name, t):
        self.name = PRIVATE_METHOD_PREFIX + name
        assert issubclass(t, Datum), 'Cannot enforce a variable that is not a Variable, Hash, or Foreign type!'
        self.type = t

    def is_of(self, v):
        if isinstance(v, self.type):
            return True
        return False


def import_module(name):
    assert not name.isdigit() and all(c.isalnum() or c == '_' for c in name), 'Invalid contract name!'
    assert name.islower(), 'Name must be lowercase!'

    _driver = rt.env.get('__Driver') or ContractDriver()
    if name in set(stdlib_list(f'{sys.version_info.major}.{sys.version_info.minor}')):
        raise ImportError

    if name.startswith('_'):
        raise ImportError

    if _driver.get_contract(name) is None:
        raise ImportError

    m = importlib.import_module(name, package=None)

    return m


def enforce_interface(m: ModuleType, interface: list):
    implemented = vars(m)

    for i in interface:
        attribute = implemented.get(i.name)
        if attribute is None:
            return False

        # Branch for data types
        if isinstance(attribute, Datum):
            if not i.is_of(attribute):
                return False

        if isinstance(attribute, FunctionType):
            if not i.is_of(attribute):
                return False
    return True


def owner_of(m: ModuleType):
    _driver = rt.env.get('__Driver') or ContractDriver()
    owner = _driver.get_var(m.__name__, OWNER_KEY)
    return owner


imports_module = ModuleType('importlib')
imports_module.import_module = import_module
imports_module.enforce_interface = enforce_interface
imports_module.Func = Func
imports_module.Var = Var
imports_module.owner_of = owner_of

exports = {
    'importlib': imports_module,
}
