import unittest
import os
import shutil
from pprint import pprint

from aistac.handlers.abstract_handlers import ConnectorContract
from aistac.properties.abstract_properties import AbstractPropertyManager
from aistac.properties.ledger_property_manager import LedgerPropertyManager


class ControlPropertyManager(AbstractPropertyManager):

    def __init__(self, task_name: str):
        root_keys = []
        knowledge_keys = []
        super().__init__(task_name, root_keys, knowledge_keys)


class MyTestCase(unittest.TestCase):

    def setUp(self):
        for task in ['first', 'second', 'third']:
            pm = ControlPropertyManager(task_name=task)
            pm.set_description(f"The {task} test manager")
            uri = f"works/aistac_pm_{pm.manager_name()}_{pm.task_name}.json"
            pm.set_property_connector(ConnectorContract(uri=uri, module_name='aistac.handlers.python_handlers', handler='PythonPersistHandler'))
            pm.set_version(f"v_{task}")
            pm.persist_properties()
            exec(f"self.pm_{task} = pm")

    def tearDown(self):
        try:
            shutil.rmtree(os.path.join(os.environ['PWD'], 'works'))
        except:
            pass

    def test_runs(self):
        """Basic smoke test"""
        LedgerPropertyManager('ledger')

    def test_get_set_ledger(self):
        master = LedgerPropertyManager('ledger')
        master.set_ledger(property_manager=self.pm_first)
        master.set_ledger(property_manager=self.pm_second)
        master.set_ledger(property_manager=self.pm_third)
        result = master.get_ledger(manager=self.pm_first.manager_name(), task=self.pm_first.task_name)
        self.assertEqual(result.get('description'), "The first test manager")
        self.assertEqual(result.get('version'), "v_first")
        result = master.get_ledger(manager=self.pm_second.manager_name(), task=self.pm_second.task_name)
        self.assertEqual(result.get('description'), "The second test manager")
        self.assertEqual(result.get('version'), "v_second")

    def test_report_ledger(self):
        master = LedgerPropertyManager('ledger')
        master.set_ledger(property_manager=self.pm_first)
        master.set_ledger(property_manager=self.pm_second)
        master.set_ledger(property_manager=self.pm_third)
        result = master.report_ledger()
        self.assertEqual(['The first test manager', 'The second test manager', 'The third test manager'], result.get('description'))
        self.assertEqual(['control', 'control', 'control'], result.get('manager_name'))
        self.assertEqual(['first', 'second', 'third'], result.get('task_name'))
        self.assertEqual(['v_first', 'v_second', 'v_third'], result.get('version'))

    def test_remove_ledger(self):
        master = LedgerPropertyManager('ledger')
        master.set_ledger(property_manager=self.pm_first)
        master.set_ledger(property_manager=self.pm_second)
        master.set_ledger(property_manager=self.pm_third)
        self.assertTrue(master.has_ledger(manager=self.pm_first.manager_name(), task=self.pm_first.task_name))
        self.assertTrue(master.has_ledger(manager=self.pm_second.manager_name(), task=self.pm_second.task_name))
        self.assertTrue(master.has_ledger(manager=self.pm_third.manager_name(), task=self.pm_third.task_name))
        # remove
        self.assertTrue(master.remove_ledger(manager=self.pm_first.manager_name(), task=self.pm_first.task_name))
        self.assertFalse(master.has_ledger(manager=self.pm_first.manager_name(), task=self.pm_first.task_name))
        self.assertTrue(master.has_ledger(manager=self.pm_second.manager_name(), task=self.pm_second.task_name))
        self.assertTrue(master.has_ledger(manager=self.pm_third.manager_name(), task=self.pm_third.task_name))
        #reset
        master.reset_ledger()
        self.assertFalse(master.has_ledger(manager=self.pm_second.manager_name(), task=self.pm_second.task_name))
        self.assertFalse(master.has_ledger(manager=self.pm_third.manager_name(), task=self.pm_third.task_name))


if __name__ == '__main__':
    unittest.main()
