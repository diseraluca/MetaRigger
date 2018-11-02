import unittest

import pymel.core
import MetaRigger.Metanodes.Metanode
import MetaRigger.Utils.TestUtils.MetariggerTestCase

class Test_testMetanodeInformations(MetaRigger.Utils.TestUtils.MetariggerTestCase.MetariggerTestCase):
    def setUp(self):
        self.metanode = MetaRigger.Metanodes.Metanode.Metanode()

    def test_TheMetanodeAddInformationMethodAddsAStringAttributeOnTheMetanodeInstance(self):
        self.assertNotHasAttr(self.metanode._metaNode, "TestId", "The metanode already has the attribute we are trying to add.")

        self.metanode.addInformation("TestId")

        self.assertHasAttr(self.metanode._metaNode, "TestId", "The new attribute wasn't added.")
        self.assertAttrIsType( self.metanode._metaNode.TestId, "string", "The new attribute isn't a string type.")

    def test_TheMetanodeAddInformationMethodAddsAWhichAttrMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "whichTestId", "The class instance already has the method we are trying to add.")

        self.metanode.addInformation("TestId")

        self.assertHasMethod(self.metanode, "whichTestId", "The new method wasn't added.")

    def test_AWhichAttrMethodReturnsTheCurrentValueStoredInTheInformationAttribute(self):
        self.metanode.addInformation("TestId")

        self.metanode._metaNode.TestId.set("192.168.0.1")
        self.assertEquals(self.metanode.whichTestId(), self.metanode._metaNode.TestId.get(), "The whichTestId method did not return the correct value (192.168.0.1).")

    def test_TheMetanodeAddInformationMethodAddsASetWhichAttrMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "setWhichTestId", "The class instance already has the method we are trying to add.")

        self.metanode.addInformation("TestId")

        self.assertHasMethod(self.metanode, "setWhichTestId", "The new method wasn't added.")

    def test_ASetWhichAttrMethodSetsTheValueStoredInTheInformationAttribute(self):
        self.metanode.addInformation("TestId")

        self.metanode.setWhichTestId("192.168.0.1")
        self.assertEquals(self.metanode._metaNode.TestId.get(), "192.168.0.1", "The whichTestId method did not set the information to the correct value.")


if __name__ == '__main__':
    unittest.main()
