import unittest
import os
import shutil

from aistac.components.abstract_ledger_component import AbstractLedger
from aistac.properties.property_manager import PropertyManager
from tests.components.abstract_component_test import ControlComponent


class MasterLedgerTest(unittest.TestCase):

    def setUp(self):
        os.environ['HADRON_PM_PATH'] = os.path.join('work', 'config')
        os.environ['HADRON_DEFAULT_PATH'] = os.path.join('work', 'data')
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('work')
        except:
            pass

    def test_smoke(self):
        """Basic smoke test"""
        AbstractLedger.from_env()

    def test_add_ledger(self):
        ledger = AbstractLedger.from_env()
        ledger.add_ledger_pm(ControlComponent.from_env('tester').pm)
        ledger.add_ledger_pm(ControlComponent.from_env('alt').pm)
        result = ledger.ledger_catalog
        self.assertEqual({'control': ['tester', 'alt']}, result)


    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
