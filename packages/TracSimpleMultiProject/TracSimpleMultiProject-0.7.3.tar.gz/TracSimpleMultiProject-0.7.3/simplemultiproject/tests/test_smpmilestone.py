import unittest
from trac.test import EnvironmentStub
from simplemultiproject.environmentSetup import smpEnvironmentSetupParticipant
from simplemultiproject.smp_model import SmpMilestone
from simplemultiproject.tests.util import revert_schema


class TestSmpMilestone(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentStub(default_data=True,
                                   enable=["trac.*", "simplemultiproject.*"])
        with self.env.db_transaction as db:
            revert_schema(self.env)
            smpEnvironmentSetupParticipant(self.env).upgrade_environment(db)
        # self.env.config.set("ticket-custom", "project", "select")
        self.model = SmpMilestone(self.env)
        self.model.add("foo1", 1)
        self.model.add("bar", 2)
        self.model.add("baz", 3)
        self.model.add("foo2", 1)

    def tearDown(self):
        self.env.reset_db()

    def test_delete(self):
        self.assertEqual(4, len(self.model.get_all_milestones_and_id_project_id()))
        self.model.delete("baz")
        self.assertEqual(3, len(self.model.get_all_milestones_and_id_project_id()))
        items = self.model.get_milestones_for_project_id(1)
        self.assertEqual(2, len(items))
        self.assertEqual("foo1", items[0])
        self.assertEqual("foo2", items[1])

    def test_add(self):
        self.assertEqual(4, len(self.model.get_all_milestones_and_id_project_id()))
        items = self.model.get_milestones_for_project_id(1)
        self.assertEqual(2, len(items))
        self.assertEqual("foo1", items[0])
        self.assertEqual("foo2", items[1])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSmpMilestone))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
