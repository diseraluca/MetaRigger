import unittest

import pymel.core
import MetaRigger.Metanodes.Metanode

class Test_MetanodeConnections(unittest.TestCase):
    def setUp(self):
        self.metanode = MetaRigger.Metanodes.Metanode.Metanode()

    def test_TheMetanodeAddConnectionMethodAddsAMessageAttributeOnTheMetanodeInstance(self):
        self.assertFalse(self.metanode._metaNode.hasAttr("Test"), "The metanode already has the attribute we are trying to add.")

        self.metanode.addConnection("Test")

        self.assertTrue(self.metanode._metaNode.hasAttr("Test"), "The new attribute wasn't added.")
        self.assertEquals( self.metanode._metaNode.Test.type() , "message", "The new attribute isn't a message type.")

    def test_TheMetanodeAddConnectionMethodMessageAttributeIsEitherAnOutputAttributeOrAnInputAttribute(self):
        self.metanode.addConnection("InputAttribute", True)
        self.assertFalse(pymel.core.general.attributeQuery(self.metanode._metaNode.InputAttribute.attrName(), node = self.metanode._metaNode.name(), readable = True), "InputAttribute should not be readable.")
        self.assertTrue(pymel.core.general.attributeQuery(self.metanode._metaNode.InputAttribute.attrName(), node = self.metanode._metaNode.name(), writable = True), "InputAttribute should be writable.")

        self.metanode.addConnection("OutputAttribute", False)
        self.assertTrue(pymel.core.general.attributeQuery(self.metanode._metaNode.OutputAttribute.attrName(), node = self.metanode._metaNode.name(), readable = True), "InputAttribute should be readable.")
        self.assertFalse(pymel.core.general.attributeQuery(self.metanode._metaNode.OutputAttribute.attrName(), node = self.metanode._metaNode.name(), writable = True), "InputAttribute should not be writable.")

    def test_TheMetanodeAddConnectionMethodAddsAWalkToAttrMethodToTheMetanodeClassInstance(self):
        self.assertFalse(hasattr(self.metanode, "walkToTest"), "The class instance already has the method we are trying to add.")

        self.metanode.addConnection("Test")

        self.assertTrue(hasattr(self.metanode, "walkToTest"), "The new method wasn't added.")

    def test_AWalkToAttrMethodReturnsTheNodeThatIsConnectedToTheRelatedAttribute(self):
        self.metanode.addConnection("Test")
        
        connectedNode = pymel.core.joint()
        connectedNode.message >> self.metanode._metaNode.Test

        self.assertEqual(self.metanode.walkToTest(), connectedNode, "The method did not return the node that is connected to the added connection.")

    def test_AWalkToAttrMethodReturnsTheFirstMadeConnectionIfItHasMultipleConnections(self):
        self.metanode.addConnection("OutputConnection", False)

        firstConnectMetanode = MetaRigger.Metanodes.Metanode.Metanode()
        firstConnectMetanode.addConnection("InputConnection")
        secondConnectMetanode = MetaRigger.Metanodes.Metanode.Metanode()
        secondConnectMetanode.addConnection("InputConnection")

        self.metanode._metaNode.OutputConnection >> firstConnectMetanode._metaNode.InputConnection
        self.metanode._metaNode.OutputConnection >> secondConnectMetanode._metaNode.InputConnection


        self.assertEqual(self.metanode.walkToOutputConnection(), firstConnectMetanode._metaNode, "The walkToAttr method did not return the first connected node.")
        
    def test_AWalkToAttrMethodReturnsNoneIfNoConnectionWasMadeToTheRelatedAttribute(self):
        self.metanode.addConnection("UnconnectedConnection")

        self.assertIsNone(self.metanode.walkToUnconnectedConnection(), "Walking on a isolated connection did not return None.")

if __name__ == '__main__':
    unittest.main()
