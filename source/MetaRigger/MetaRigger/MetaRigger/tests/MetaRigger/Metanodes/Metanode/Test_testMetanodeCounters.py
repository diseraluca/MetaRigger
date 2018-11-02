import unittest

import pymel.core
import MetaRigger.Metanodes.Metanode
import MetaRigger.Utils.TestUtils.MetariggerTestCase

class Test_Test_testMetanodeCounters(MetaRigger.Utils.TestUtils.MetariggerTestCase.MetariggerTestCase):
    def setUp(self):
        self.metanode = MetaRigger.Metanodes.Metanode.Metanode()

    def test_TheMetanodeAddCounterMethodAddsAFloatAttributeOnTheMetanodeInstance(self):
        self.assertNotHasAttr(self.metanode._metaNode, "Tests", "The metanode already has the attribute we are trying to add.")

        self.metanode.addCounter("Tests")

        self.assertHasAttr(self.metanode._metaNode, "Tests", "The new attribute wasn't added.")
        self.assertAttrIsType( self.metanode._metaNode.Tests, "float", "The new attribute isn't a float type.")

    def test_TheMetanodeAddCounterMethodAddsAnHowManyAttrMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "howManyTests", "The class instance already has the method we are trying to add.")

        self.metanode.addCounter("Tests")

        self.assertHasMethod(self.metanode, "howManyTests", "The new method wasn't added.")

    def test_AnIsAttrMethodReturnsTheCurrentValueStoredInTheOptionAttribute(self):
        self.metanode.addCounter("Tests")

        self.assertEquals(self.metanode.howManyTests(), self.metanode._metaNode.Tests.get(), "The howManyTests method did not return the correct value (0.0).")
        self.metanode._metaNode.Tests.set(0.5)
        self.assertEquals(self.metanode.howManyTests(), self.metanode._metaNode.Tests.get(), "The howManyTests method did not return the correct value (0.5).")

    def test_TheMetanodeAddCounterMethodAddsAnSetHowManyAttrMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "setHowManyTests", "The class instance already has the method we are trying to add.")

        self.metanode.addCounter("Tests")

        self.assertHasMethod(self.metanode, "setHowManyTests", "The new method wasn't added.")

    def test_ASetHowManyAttrMethodSetsTheValueStoredInTheCounterAttribute(self):
        self.metanode.addCounter("Tests")

        self.metanode.setHowManyTests(0.5)
        self.assertEquals(self.metanode._metaNode.Tests.get(), 0.5, "The setHowManyTests method did not set the counter to the correct value.")

    def test_ASetHowManyAttrMethodSetsTheValueStoredInTheCounterAttributeToTheMaxPossibleValueIfAGreaterValueIsSetted(self):
        self.metanode.addCounter("Tests", max = 2.0)

        self.metanode.setHowManyTests(3.0)
        self.assertEquals(self.metanode._metaNode.Tests.get(), 2.0, "The setHowManyTests method did not set the counter to the correct max value.")

    def test_ASetHowManyAttrMethodSetsTheValueStoredInTheCounterAttributeToTheMinPossibleValueIfALowerValueIsSetted(self):
        self.metanode.addCounter("Tests", min = 0.5)

        self.metanode.setHowManyTests(0.0)
        self.assertEquals(self.metanode._metaNode.Tests.get(), 0.5, "The setHowManyTests method did not set the counter to the correct min value.")

if __name__ == '__main__':
    unittest.main()
