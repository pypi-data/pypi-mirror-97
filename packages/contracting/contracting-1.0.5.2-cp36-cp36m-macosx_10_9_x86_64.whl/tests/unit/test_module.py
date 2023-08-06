from unittest import TestCase
from contracting.execution.module import *
import types
import glob


class TestDatabase(TestCase):
    def setUp(self):
        self.d = ContractDriver()
        self.d.flush()

    def tearDown(self):
        self.d.flush()

    def test_push_and_get_contract(self):
        code = 'a = 123'
        name = 'test'

        self.d.set_contract(name, code)
        _code = self.d.get_contract(name)

        self.assertEqual(code, _code, 'Pushing and getting contracts is not working.')

    def test_flush(self):
        code = 'a = 123'
        name = 'test'

        self.d.set_contract(name, code)
        self.d.commit()
        self.d.flush()

        self.assertIsNone(self.d.get_contract(name))


class TestDatabaseLoader(TestCase):
    def setUp(self):
        self.dl = DatabaseLoader()

    def test_init(self):
        self.assertTrue(isinstance(self.dl.d, ContractDriver), 'self.d is not a Database object.')

    def test_create_module(self):
        self.assertEqual(self.dl.create_module(None), None, 'self.create_module should return None')

    def test_exec_module(self):
        module = types.ModuleType('test')

        self.dl.d.set_contract('test', 'b = 1337')
        self.dl.exec_module(module)
        self.dl.d.flush()

        self.assertEqual(module.b, 1337)

    def test_exec_module_nonattribute(self):
        module = types.ModuleType('test')

        self.dl.d.set_contract('test', 'b = 1337')
        self.dl.exec_module(module)
        self.dl.d.flush()

        with self.assertRaises(AttributeError):
            module.a

    def test_module_representation(self):
        module = types.ModuleType('howdy')

        self.assertEqual(self.dl.module_repr(module), "<module 'howdy' (smart contract)>")


class TestInstallLoader(TestCase):
    def test_install_loader(self):
        uninstall_database_loader()

        self.assertNotIn(DatabaseFinder, sys.meta_path)

        install_database_loader()

        self.assertIn(DatabaseFinder, sys.meta_path)

        uninstall_database_loader()

        self.assertNotIn(DatabaseFinder, sys.meta_path)

    def test_integration_and_importing(self):
        dl = DatabaseLoader()
        dl.d.set_contract('testing', 'a = 1234567890')
        dl.d.commit()

        install_database_loader()

        import testing

        #dl.d.flush()

        self.assertEqual(testing.a, 1234567890)


driver = ContractDriver()


class TestModuleLoadingIntegration(TestCase):
    def setUp(self):
        sys.meta_path.append(DatabaseFinder)
        driver.flush()
        contracts = glob.glob('./test_sys_contracts/*.py')
        for contract in contracts:
            name = contract.split('/')[-1]
            name = name.split('.')[0]

            with open(contract) as f:
                code = f.read()

            driver.set_contract(name=name, code=code)
            driver.commit()

    def tearDown(self):
        sys.meta_path.remove(DatabaseFinder)
        driver.flush()

    def test_get_code_string(self):
        ctx = types.ModuleType('ctx')
        code = '''import module1

print("now i can run my functions!")
'''

        exec(code, vars(ctx))

        print('ok do it again')

        exec(code, vars(ctx))
