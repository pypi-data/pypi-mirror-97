import datetime
import unittest

from ofxReaderBR.model import BankStatement, CashFlow, CashFlowType, Origin


class BankStatementTestCase(unittest.TestCase):

    def test_add_when_one_has_error_status_and_the_other_has_complete_status(self):
        bs_error = BankStatement(file=None)
        bs_error.read_status = BankStatement.ERROR
        bs_complete = BankStatement(file=None)
        bs_complete.read_status = BankStatement.COMPLETE

        bs = bs_complete + bs_error

        self.assertEqual(BankStatement.ERROR, bs.read_status)


class CashFlowTestCase(unittest.TestCase):

    def test_is_valid_return_false_when_accrual_date_greater_than_cash_date(
            self):
        cf = CashFlow(name='Test cash flow',
                      flow_type=CashFlowType.CREDIT,
                      value=42.0,
                      accrual_date=datetime.datetime(2019, 11, 23),
                      cash_date=datetime.datetime(1981, 11, 23),
                      origin=Origin(account_id="1", type='BANKACCOUNT'))
        self.assertFalse(cf.is_valid())

    def test_is_valid_return_false_when_origin_is_none(self):
        cf = CashFlow(
            name='Test cash flow',
            flow_type=CashFlowType.DEBIT,
            value=-42.0,
            accrual_date=datetime.datetime(2019, 11, 22),
            cash_date=datetime.datetime(2019, 11, 23),
        )
        self.assertFalse(cf.is_valid())

    def test_is_valid_return_true(self):
        today = datetime.datetime.today()
        origin = Origin(account_id='125668',
                        branch='1235',
                        institution='0261',
                        type='BANKACCOUNT')
        cf = CashFlow('Test', CashFlowType.CREDIT, 42.0, today, today, origin)
        self.assertTrue(cf.is_valid())


class OriginTestCase(unittest.TestCase):

    def test_raise_value_error_when_type_is_none(self):
        with self.assertRaises(ValueError):
            Origin(type=None)

    def test_is_bank_account_return_false_when_type_credit_card(self):
        origin = Origin(type='CREDITCARD')
        self.assertFalse(origin.is_bank_account())

    def test_is_bank_account_return_true_when_type_bank_account(self):
        origin = Origin(type='BANKACCOUNT')
        self.assertTrue(origin.is_bank_account())


if __name__ == '__main__':
    unittest.main()
