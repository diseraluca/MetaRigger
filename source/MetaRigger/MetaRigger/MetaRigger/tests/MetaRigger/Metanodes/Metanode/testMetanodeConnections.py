import unittest

import pymel.core
import MetaRigger.Metanodes.Metanode
import MetaRigger.Utils.TestUtils.MetariggerTestCase

class Test_MetanodeConnections(MetaRigger.Utils.TestUtils.MetariggerTestCase.MetariggerTestCase):
    def setUp(self):
        self.metanode = MetaRigger.Metanodes.Metanode.Metanode()

    def test_TheMetanodeAddConnectionMethodAddsAMessageAttributeOnTheMetanodeInstance(self):
        self.assertNotHasAttr(self.metanode._metaNode, "Test", "The metanode already has the attribute we are trying to add.")

        self.metanode.addConnection("Test")

        self.assertHasAttr(self.metanode._metaNode, "Test", "The new attribute wasn't added.")
        self.assertAttrIsType( self.metanode._metaNode.Test, "message", "The new attribute isn't a message type.")

    def test_TheMetanodeAddConnectionMethodMessageAttributeIsEitherAnOutputAttributeOrAnInputAttribute(self):
        self.metanode.addConnection("InputAttribute", True)
        self.assertAttrIsNotReadable(self.metanode._metaNode.InputAttribute, "InputAttribute should not be readable.")
        self.assertAttrIsWritable(self.metanode._metaNode.InputAttribute, "InputAttribute should be writable.")

        self.metanode.addConnection("OutputAttribute", False)
        self.assertAttrIsReadable(self.metanode._metaNode.OutputAttribute, "InputAttribute should be readable.")
        self.assertAttrIsNotWritable(self.metanode._metaNode.OutputAttribute, "InputAttribute should not be writable.")

    def test_TheMetanodeAddConnectionMethodAddsAWalkToAttrMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "walkToTest", "The class instance already has the method we are trying to add.")

        self.metanode.addConnection("Test")

        self.assertHasMethod(self.metanode, "walkToTest", "The new method wasn't added.")

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

    def test_TheMetanodeAddConnectionMethodAddsAisAttrConnectedMethodToTheMetanodeClassInstance(self):
        self.assertNotHasMethod(self.metanode, "isTestConnected", "The class instance already has the method we are trying to add.")

        self.metanode.addConnection("Test")

        self.assertHasMethod(self.metanode, "isTestConnected", "The new method wasn't added.")

    def test_AnIsAttrConnectedMethodReturnsWhetherTheAttrHasAnyConnection(self):
        self.metanode.addConnection("Test")

        self.assertFalse(self.metanode.isTestConnected())
        self.metanode._metaNode._childs >> self.metanode._metaNode.Test
        self.assertTrue(self.metanode.isTestConnected())

    def test_TheMetanodeAddConnectionMethodSavesTheNameOfTheNewlyConstructedAttributeInTheMetanodeClassInstance_connectionsMember(self):
        self.metanode.addConnection("Test")

        self.assertListEqual(self.metanode._connections, ["Test"], "The connection wasn't stored in _connections.")

    def test_TheMetanodeListConnectionsMethodReturnsAListOfConnectionsNamesThatWereAdded(self):
        self.metanode.addConnection("Test")
        self.metanode.addConnection("Test2")

        self.assertListEqual(self.metanode.listConnections(), ["Test", "Test2"], "listConnections didn't return the correct list of names.")

if __name__ == '__main__':
    unittest.main()
