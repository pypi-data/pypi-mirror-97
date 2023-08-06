from unittest import TestCase
from contracting.db.driver import ContractDriver
from contracting.execution.executor import Executor
from datetime import datetime
from contracting.stdlib.env import gather
from hashlib import sha256, sha3_256

def submission_kwargs_for_file(f):
    # Get the file name only by splitting off directories
    split = f.split('/')
    split = split[-1]

    # Now split off the .s
    split = split.split('.')
    contract_name = split[0]

    with open(f) as file:
        contract_code = file.read()

    return {
        'name': contract_name,
        'code': contract_code,
    }


TEST_SUBMISSION_KWARGS = {
    'sender': 'stu',
    'contract_name': 'submission',
    'function_name': 'submit_contract'
}


class TestComplexContracts(TestCase):
    def setUp(self):
        self.d = ContractDriver()
        self.d.flush()

        with open('../../contracting/contracts/submission.s.py') as f:
            contract = f.read()

        self.d.set_contract(name='submission',
                            code=contract)
        self.d.commit()

    def tearDown(self):
        self.d.flush()

    def test_token_constuction_works(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/currency.s.py'))

        res = e.execute('stu', 'currency', 'balance', kwargs={'account': 'colin'})
        self.assertEqual(res['result'], 100)

        print(res)

        res = e.execute('stu', 'currency', 'balance', kwargs={'account': 'stu'})
        self.assertEqual(res['result'], 1000000)

        res = e.execute('stu', 'currency', 'balance', kwargs={'account': 'raghu'})
        self.assertEqual(res['result'], None)

    def test_token_transfer_works(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/currency.s.py'))

        e.execute('stu', 'currency', 'transfer', kwargs={'amount': 1000, 'to': 'colin'})

        stu_balance = e.execute('stu', 'currency', 'balance', kwargs={'account': 'stu'})
        colin_balance = e.execute('stu', 'currency', 'balance', kwargs={'account': 'colin'})

        self.assertEqual(stu_balance['result'], 1000000 - 1000)
        self.assertEqual(colin_balance['result'], 100 + 1000)

    def test_token_transfer_failure_not_enough_to_send(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/currency.s.py'))

        status = e.execute('stu', 'currency', 'transfer', kwargs={'amount': 1000001, 'to': 'colin'})

        self.assertEqual(status['status_code'], 1)

    def test_token_transfer_to_new_account(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/currency.s.py'))

        e.execute('stu', 'currency', 'transfer', kwargs={'amount': 1000, 'to': 'raghu'})

        raghu_balance = e.execute('stu', 'currency', 'balance', kwargs={'account': 'raghu'})

        self.assertEqual(raghu_balance['result'], 1000)

    def test_erc20_clone_construction_works(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/erc20_clone.s.py'))

        stu = e.execute('stu', 'erc20_clone', 'balance_of', kwargs={'account': 'stu'})
        colin = e.execute('stu', 'erc20_clone', 'balance_of', kwargs={'account': 'colin'})
        supply = e.execute('stu', 'erc20_clone', 'total_supply', kwargs={})

        self.assertEqual(stu['result'], 1000000)
        self.assertEqual(colin['result'], 100)
        self.assertEqual(supply['result'], 1000100)

    def test_erc20_clone_transfer_works(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/erc20_clone.s.py'))

        e.execute('stu', 'erc20_clone', 'transfer', kwargs={'amount': 1000000, 'to': 'raghu'})
        raghu = e.execute('stu', 'erc20_clone', 'balance_of', kwargs={'account': 'raghu'})
        stu = e.execute('stu', 'erc20_clone', 'balance_of', kwargs={'account': 'stu'})

        self.assertEqual(raghu['result'], 1000000)
        self.assertEqual(stu['result'], 0)

    def test_erc20_clone_transfer_fails(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/erc20_clone.s.py'))

        output = e.execute('stu', 'erc20_clone', 'transfer', kwargs={'amount': 10000000, 'to': 'raghu'})

        self.assertEqual(output['status_code'], 1)
        self.assertEqual(type(output['result']), AssertionError)

    def test_allowance_of_blank(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/erc20_clone.s.py'))

        output = e.execute('stu', 'erc20_clone', 'allowance', kwargs={'owner': 'stu', 'spender': 'raghu'})
        self.assertEqual(output['result'], 0)

    def test_approve_works_and_allowance_shows(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/erc20_clone.s.py'))

        e.execute('stu', 'erc20_clone', 'approve', kwargs={'amount': 1234, 'to': 'raghu'})

        output = e.execute('stu', 'erc20_clone', 'allowance', kwargs={'owner': 'stu', 'spender': 'raghu'})
        self.assertEqual(output['result'], 1234)

    def test_approve_and_transfer_from(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/erc20_clone.s.py'))

        e.execute('stu', 'erc20_clone', 'approve', kwargs={'amount': 1234, 'to': 'raghu'})
        e.execute('raghu', 'erc20_clone', 'transfer_from', kwargs={'amount': 123, 'to': 'tejas', 'main_account': 'stu'})
        raghu = e.execute('stu', 'erc20_clone', 'balance_of', kwargs={'account': 'raghu'})
        stu = e.execute('stu', 'erc20_clone', 'balance_of', kwargs={'account': 'stu'})
        tejas = e.execute('stu', 'erc20_clone', 'balance_of', kwargs={'account': 'tejas'})

        self.assertEqual(raghu['result'], 0)
        self.assertEqual(stu['result'], (1000000 - 123))
        self.assertEqual(tejas['result'], 123)

    def test_failure_after_data_writes_doesnt_commit(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/leaky.s.py'), auto_commit=True)

        e.execute('colin', 'leaky', 'transfer', kwargs={'amount': 1234, 'to': 'raghu'}, auto_commit=True)

        raghu = e.execute('stu', 'leaky', 'balance_of', kwargs={'account': 'raghu'}, auto_commit=True)
        colin = e.execute('stu', 'leaky', 'balance_of', kwargs={'account': 'colin'}, auto_commit=True)

        self.assertEqual(raghu['result'], 0)
        self.assertEqual(colin['result'], 100)

    def test_leaky_contract_commits_on_success(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/leaky.s.py'))

        e.execute('colin', 'leaky', 'transfer', kwargs={'amount': 1, 'to': 'raghu'})

        raghu = e.execute('stu', 'leaky', 'balance_of', kwargs={'account': 'raghu'})
        colin = e.execute('stu', 'leaky', 'balance_of', kwargs={'account': 'colin'})

        self.assertEqual(raghu['result'], 1)
        self.assertEqual(colin['result'], 99)

    def test_time_stdlib_works(self):
        e = Executor(metering=False)
        now = datetime.now()

        environment = gather()
        date = environment['datetime'].datetime(now.year, now.month, now.day)
        environment.update({'now': date})

        res = e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/test_time.s.py'),
                  environment=environment)

        gt = e.execute('colin', 'test_time', 'gt', kwargs={}, environment=environment)
        self.assertTrue(gt['result'])

        lt = e.execute('colin', 'test_time', 'lt', kwargs={}, environment=environment)
        self.assertFalse(lt['result'])

        eq = e.execute('colin', 'test_time', 'eq', kwargs={}, environment=environment)
        self.assertFalse(eq['result'])

    def test_bad_time_contract_not_submittable(self):
        e = Executor(metering=False)
        now = datetime.now()

        environment = gather()
        date = environment['datetime'].datetime(now.year, now.month, now.day)
        environment.update({'now': date})

        output = e.execute(**TEST_SUBMISSION_KWARGS,
                           kwargs=submission_kwargs_for_file('./test_contracts/bad_time.s.py'),
                           environment=environment)

        self.assertEqual(output['status_code'], 1)

    def test_json_lists_work(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                    kwargs=submission_kwargs_for_file('./test_contracts/json_tests.s.py'))

        res = e.execute('colin', 'json_tests', 'get_some', kwargs={})

        self.assertListEqual([1, 2, 3, 4], res['result'])

    def test_time_storage_works(self):
        e = Executor(metering=False)

        environment = gather()

        e.execute(**TEST_SUBMISSION_KWARGS,
                           kwargs=submission_kwargs_for_file('./test_contracts/time_storage.s.py'))

        v = e.execute('colin', 'time_storage', 'get', kwargs={})

        date = environment['datetime'].datetime(2019, 1, 1)

        self.assertEqual(v['result'], date)

    def test_hash_sha3_works(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/test_hashing_works.s.py'))

        secret = 'c0d1cc254c2aca8716c6ef170630550d'
        s3 = e.execute('colin', 'test_hashing_works', 't_sha3', kwargs={'s': secret})

        h = sha3_256()
        h.update(bytes.fromhex(secret))
        self.assertEqual(h.hexdigest(), s3['result'])

    def test_hash_sha256_works(self):
        e = Executor(metering=False)

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('./test_contracts/test_hashing_works.s.py'))

        secret = 'c0d1cc254c2aca8716c6ef170630550d'
        s3 = e.execute('colin', 'test_hashing_works', 't_sha256', kwargs={'s': secret})

        h = sha256()
        h.update(bytes.fromhex(secret))
        self.assertEqual(h.hexdigest(), s3['result'])