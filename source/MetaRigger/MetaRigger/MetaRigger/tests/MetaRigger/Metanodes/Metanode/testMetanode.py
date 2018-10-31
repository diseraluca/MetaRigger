import unittest
import inspect

import pymel.core
import MetaRigger.Metanodes.Metanode


class Test_testMetanode(unittest.TestCase):
    def setUp(self):
        self.metanode = MetaRigger.Metanodes.Metanode.Metanode()

    def test_AMetanodeCreatesAnEmptyMayaNodeWhenInstanciated(self):
        count = len(pymel.core.ls(type = 'unknown'))
        MetaRigger.Metanodes.Metanode.Metanode()

        self.assertEqual(len(pymel.core.ls(type = 'unknown')), count + 1, "The Metanode did not create an unknown node.")

    def test_AMetanodeStoresTheNewlyCreatedUnknownNodeAsAnInstanceMember(self):
        self.assertIsInstance(self.metanode._metaNode, pymel.core.nodetypes.Unknown, "The metanode isn't storing an Uknown node in its member.")

    def test_AMetanodeStoresAPyNodeDerivedClassInIts_typeMember(self):
        self.assertTrue( inspect.isclass(self.metanode._type), "The _type member isn't storing a class.")
        self.assertTrue( issubclass(self.metanode._type, pymel.core.general.PyNode), "The _type member isn't storing an child of PyNode." )

    def test_TheMetanodeConstructorRaisesATypeErrorExceptionIfTheTypeArgumentIsntAClassDerivedFromPyNode(self):
        self.assertRaises(TypeError, MetaRigger.Metanodes.Metanode.Metanode, type = 'notAPynodeClassOrAClassAtAll')
        self.assertRaises(TypeError, MetaRigger.Metanodes.Metanode.Metanode, type = int)

    def test_TheMetanodeEncapsulatedUnknownNodeHasAStringAttributeCalled_Type(self):
        self.assertTrue( self.metanode._metaNode.hasAttr("_type"), "The Metanode._metanode node has no type attribute.")
        self.assertEquals( self.metanode._metaNode._type.type() , "string", "The type attribute isn't a string type.")

    def test_TheMetanodeEncapsulatedUnknownNodeHasAInputMessageAttributeCalled_Instance(self):
        self.assertTrue( self.metanode._metaNode.hasAttr("_instance"), "The Metanode._metanode node has no _instance attribute.")
        self.assertEquals( self.metanode._metaNode._instance.type() , "message", "The _instance attribute isn't a message type.")

        self.assertFalse(pymel.core.general.attributeQuery(self.metanode._metaNode._instance.attrName(), node = self.metanode._metaNode.name(), readable = True), "The _instance attribute should not be readable.")
        self.assertTrue(pymel.core.general.attributeQuery(self.metanode._metaNode._instance.attrName(), node = self.metanode._metaNode.name(), writable = True), "The _instance attribute should be writable.")

    def test_TheMetanodeEncapsulatedUnknownNodeHasAInputMessageAttributeCalled_Parent(self):
        self.assertTrue( self.metanode._metaNode.hasAttr("_parent"), "The Metanode._metanode node has no _parent attribute.")
        self.assertEquals( self.metanode._metaNode._parent.type() , "message", "The _parent attribute isn't a message type.")

        self.assertFalse(pymel.core.general.attributeQuery(self.metanode._metaNode._instance.attrName(), node = self.metanode._metaNode.name(), readable = True), "The _parent attribute should not be readable.")
        self.assertTrue(pymel.core.general.attributeQuery(self.metanode._metaNode._instance.attrName(), node = self.metanode._metaNode.name(), writable = True), "The _parent attribute should be writable.")

    def test_TheMetanodeEncapsulatedUnknownNodeHasAnOutputMessageAttributeCalled_Childs(self):
        self.assertTrue( self.metanode._metaNode.hasAttr("_childs"), "The Metanode._metanode node has no _childs attribute.")
        self.assertEquals( self.metanode._metaNode._childs.type() , "message", "The _childs attribute isn't a message type.")

        self.assertTrue(pymel.core.general.attributeQuery(self.metanode._metaNode._childs.attrName(), node = self.metanode._metaNode.name(), readable = True), "The _childs attribute should be readable.")
        self.assertFalse(pymel.core.general.attributeQuery(self.metanode._metaNode._childs.attrName(), node = self.metanode._metaNode.name(), writable = True), "The _childs attribute should not be writable.")

    def test_TheMetanodeBuildMethodShouldInstanciateANodeOfTheTypeStoredIn_Type(self):
        builtNode = self.metanode.build()

        self.assertIsInstance(builtNode, self.metanode._type, "The newly built node is not an instance of the class stored in _type.");

    def test_TheMetanodeBuildMethodShouldStoreAReferenceToTheNewlyInstanciatedNodeInIts_InstanceMember(self):
        builtNode = self.metanode.build()

        self.assertIs(self.metanode._instance, builtNode, "The _instance member is not holding a reference to the newly created node.")

    def test_TheMetanodeBuildMethodShouldNotCreateANewNodeIfTheNodeIsAlreadyBeenBuilt(self):
        self.metanode.build()
        count = len(pymel.core.ls())
        self.metanode.build()

        self.assertEqual(len(pymel.core.ls()), count, "The second call to build has created a new node.")

if __name__ == '__main__':
    unittest.main()