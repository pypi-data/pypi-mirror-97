from unittest import TestCase
from contracting.stdlib.bridge.time import Datetime
from contracting.client import ContractingClient


class TestDynamicImports(TestCase):
    def setUp(self):
        self.c = ContractingClient(signer='stu')
        self.c.raw_driver.flush()

        with open('../../contracting/contracts/submission.s.py') as f:
            contract = f.read()

        self.c.raw_driver.set_contract(name='submission', code=contract)

        self.c.raw_driver.commit()

        # submit erc20 clone
        with open('./test_contracts/stubucks.s.py') as f:
            code = f.read()
            self.c.submit(code, name='stubucks')

        with open('./test_contracts/tejastokens.s.py') as f:
            code = f.read()
            self.c.submit(code, name='tejastokens')

        with open('./test_contracts/bastardcoin.s.py') as f:
            code = f.read()
            self.c.submit(code, name='bastardcoin')

        with open('./test_contracts/dynamic_importing.s.py') as f:
            code = f.read()
            self.c.submit(code, name='dynamic_importing')

        self.stubucks = self.c.get_contract('stubucks')
        self.tejastokens = self.c.get_contract('tejastokens')
        self.bastardcoin = self.c.get_contract('bastardcoin')
        self.dynamic_importing = self.c.get_contract('dynamic_importing')

    def tearDown(self):
        self.c.raw_driver.flush()

    def test_successful_submission(self):
        self.assertEqual(self.stubucks.balance_of(account='stu'), 123)
        self.assertEqual(self.stubucks.balance_of(account='colin'), 321)

        self.assertEqual(self.tejastokens.balance_of(account='stu'), 321)
        self.assertEqual(self.tejastokens.balance_of(account='colin'), 123)

        self.assertEqual(self.bastardcoin.balance_of(account='stu'), 999)
        self.assertEqual(self.bastardcoin.balance_of(account='colin'), 555)

    def test_get_stubuck_balances(self):
        stu = self.dynamic_importing.balance_for_token(tok='stubucks', account='stu')
        colin = self.dynamic_importing.balance_for_token(tok='stubucks', account='colin')

        self.assertEqual(stu, 123)
        self.assertEqual(colin, 321)

    def test_get_tejastokens_balances(self):
        stu = self.dynamic_importing.balance_for_token(tok='tejastokens', account='stu')
        colin = self.dynamic_importing.balance_for_token(tok='tejastokens', account='colin')

        self.assertEqual(stu, 321)
        self.assertEqual(colin, 123)

    def test_get_bastardcoin_balances(self):
        stu = self.dynamic_importing.balance_for_token(tok='bastardcoin', account='stu')
        colin = self.dynamic_importing.balance_for_token(tok='bastardcoin', account='colin')

        self.assertEqual(stu, 999)
        self.assertEqual(colin, 555)

    def test_is_erc20(self):
        self.assertTrue(self.dynamic_importing.is_erc20_compatible(tok='stubucks'))
        self.assertTrue(self.dynamic_importing.is_erc20_compatible(tok='tejastokens'))
        self.assertFalse(self.dynamic_importing.is_erc20_compatible(tok='bastardcoin'))

    def test_get_balances_erc20_enforced_stubucks(self):
        stu = self.dynamic_importing.only_erc20(tok='stubucks', account='stu')
        colin = self.dynamic_importing.only_erc20(tok='stubucks', account='colin')

        self.assertEqual(stu, 123)
        self.assertEqual(colin, 321)

    def test_get_balances_erc20_enforced_tejastokens(self):
        stu = self.dynamic_importing.only_erc20(tok='tejastokens', account='stu')
        colin = self.dynamic_importing.only_erc20(tok='tejastokens', account='colin')

        self.assertEqual(stu, 321)
        self.assertEqual(colin, 123)

    def test_erc20_enforced_fails_for_bastardcoin(self):
        with self.assertRaises(AssertionError):
            stu = self.dynamic_importing.only_erc20(tok='bastardcoin', account='stu')

    def test_owner_of_returns_default(self):
        with open('./test_contracts/owner_stuff.s.py') as f:
            code = f.read()
            self.c.submit(code, name='owner_stuff', owner='poo')

        owner_stuff = self.c.get_contract('owner_stuff')

        self.assertIsNone(owner_stuff.get_owner(s='stubucks', signer='poo'))
        self.assertEqual(owner_stuff.get_owner(s='owner_stuff', signer='poo'), 'poo')

    def test_ctx_owner_works(self):
        with open('./test_contracts/owner_stuff.s.py') as f:
            code = f.read()
            self.c.submit(code, name='owner_stuff', owner='poot')

        owner_stuff = self.c.get_contract('owner_stuff')

        self.assertEqual(owner_stuff.owner_of_this(signer='poot'), 'poot')

    def test_incorrect_owner_prevents_function_call(self):
        with open('./test_contracts/owner_stuff.s.py') as f:
            code = f.read()
            self.c.submit(code, name='owner_stuff', owner='poot')

        owner_stuff = self.c.get_contract('owner_stuff')
        with self.assertRaises(Exception):
            owner_stuff.owner_of_this()

    def test_delegate_call_with_owner_works(self):
        with open('./test_contracts/parent_test.s.py') as f:
            code = f.read()
            self.c.submit(code, name='parent_test')

        with open('./test_contracts/child_test.s.py') as f:
            code = f.read()
            self.c.submit(code, name='child_test', owner='parent_test')

        parent_test = self.c.get_contract('parent_test')

        val = parent_test.get_val_from_child(s='child_test')

        self.assertEqual(val, 'good')

    def test_delegate_with_wrong_owner_does_not_work(self):
        with open('./test_contracts/parent_test.s.py') as f:
            code = f.read()
            self.c.submit(code, name='parent_test')

        with open('./test_contracts/child_test.s.py') as f:
            code = f.read()
            self.c.submit(code, name='child_test', owner='blorg')

        parent_test = self.c.get_contract('parent_test')

        with self.assertRaises(Exception) as e:
            parent_test.get_val_from_child(s='child_test')
