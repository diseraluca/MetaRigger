import unittest

import pymel.core
import MetaRigger.Metanodes.Metanode
import MetaRigger.Utils.TestUtils.MetariggerTestCase

class Test_testMetanodeOptions(MetaRigger.Utils.TestUtils.MetariggerTestCase.MetariggerTestCase):
    def setUp(self):
        self.metanode = MetaRigger.Metanodes.Metanode.Metanode()

    def test_TheMetanodeAddOptionMethodAddsBooleanAttributeOnTheMetanodeInstance(self):
        self.assertNotHasAttr(self.metanode._metaNode, "Test", "The metanode already has the attribute we are trying to add.")

        self.metanode.addOption("Test")

        self.assertHasAttr(self.metanode._metaNode, "Test", "The new attribute wasn't added.")
        self.assertAttrIsType( self.metanode._metaNode.Test, "bool", "The new attribute isn't a boolean type.")

    def test_TheMetanodeAddOptionMethodAddsAIsAttrMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "isTestable", "The class instance already has the method we are trying to add.")

        self.metanode.addOption("Testable")

        self.assertHasMethod(self.metanode, "isTestable", "The new method wasn't added.")

    def test_AnIsAttrMethodReturnsTheCurrentValueStoredInTheOptionAttribute(self):
        self.metanode.addOption("Testable")

        self.assertEquals(self.metanode.isTestable(), self.metanode._metaNode.Testable.get(), "The isTestable method did not return the correct value (True).")
        self.metanode._metaNode.Testable.set(False)
        self.assertEquals(self.metanode.isTestable(), self.metanode._metaNode.Testable.get(), "The isTestable method did not return the correct value (False).")

    def test_TheMetanodeAddOptionMethodAddsAsetAttrMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "setTestable", "The class instance already has the method we are trying to add.")

        self.metanode.addOption("Testable")

        self.assertHasMethod(self.metanode, "setTestable", "The new method wasn't added.")

    def test_ASetAttrMethodSetsTheValueStoredInTheOptionAttribute(self):
        self.metanode.addOption("Testable")

        self.metanode.setTestable(False)
        self.assertEquals(self.metanode._metaNode.Testable.get(), False, "The setTestable method did not set the option to False.")

if __name__ == '__main__':
    unittest.main()
