from unittest import TestCase
import secrets
from contracting.db.driver import ContractDriver
from contracting.execution.executor import Executor


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


class TestSandbox(TestCase):
    def setUp(self):
        self.d = ContractDriver()
        self.d.flush()

        with open('../../contracting/contracts/submission.s.py') as f:
            contract = f.read()

        self.d.set_contract(name='submission',
                            code=contract,
                            author='sys')
        self.d.commit()

        self.recipients = [secrets.token_hex(16) for _ in range(10000)]

    def tearDown(self):
        self.d.flush()

    def test_transfer_performance(self):
        e = Executor()

        e.execute(**TEST_SUBMISSION_KWARGS,
                  kwargs=submission_kwargs_for_file('../integration/test_contracts/erc20_clone.s.py'))

        for r in self.recipients:
            e.execute(sender='stu',
                      contract_name='erc20_clone',
                      function_name='transfer',
                      kwargs={
                          'amount': 1,
                          'to': r
                      })