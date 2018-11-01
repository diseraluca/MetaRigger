import unittest
import inspect

import pymel.core
import MetaRigger.Metanodes.Metanode
import MetaRigger.Utils.TestUtils.MetariggerTestCase

class Test_testMetanode(MetaRigger.Utils.TestUtils.MetariggerTestCase.MetariggerTestCase):
    def setUp(self):
        self.metanode = MetaRigger.Metanodes.Metanode.Metanode()

    def test_AMetanodeCreatesAnEmptyMayaNodeWhenInstanciated(self):
        count = len(pymel.core.ls(type = 'unknown'))
        MetaRigger.Metanodes.Metanode.Metanode()

        self.assertEqual(len(pymel.core.ls(type = 'unknown')), count + 1, "The Metanode did not create an unknown node.")

    def test_AMetanodeStoresTheNewlyCreatedUnknownNodeAsAnInstanceMember(self):
        self.assertIsInstance(self.metanode._metaNode, pymel.core.nodetypes.Unknown, "The metanode isn't storing an Uknown node in its member.")

    def test_AMetanodeStoresAPyNodeDerivedClassInIts_typeMember(self):
        self.assertIsClass( self.metanode._type, "The _type member isn't storing a class.")
        self.assertIsSubClass( self.metanode._type, pymel.core.general.PyNode, "The _type member isn't storing an child of PyNode." )

    def test_TheMetanodeConstructorRaisesATypeErrorExceptionIfTheTypeArgumentIsntAClassDerivedFromPyNode(self):
        self.assertRaises(TypeError, MetaRigger.Metanodes.Metanode.Metanode, type = 'notAPynodeClassOrAClassAtAll')
        self.assertRaises(TypeError, MetaRigger.Metanodes.Metanode.Metanode, type = int)

    def test_TheMetanodeEncapsulatedUnknownNodeHasAStringAttributeCalled_Type(self):
        self.assertHasAttr( self.metanode._metaNode, "_type", "The Metanode._metanode node has no _type attribute.")
        self.assertAttrIsType( self.metanode._metaNode._type , "string", "The _type attribute isn't a string type.")

    def test_TheMetanodeEncapsulatedUnknownNodeHasAInputMessageAttributeCalled_Instance(self):
        self.assertHasAttr( self.metanode._metaNode, "_instance", "The Metanode._metanode node has no _instance attribute.")
        self.assertAttrIsType( self.metanode._metaNode._instance , "message", "The _instance attribute isn't a message type.")

        self.assertAttrIsNotReadable(self.metanode._metaNode._instance, "The _instance attribute should not be readable.")
        self.assertAttrIsWritable(self.metanode._metaNode._instance, "The _instance attribute should be writable.")

    def test_TheMetanodeEncapsulatedUnknownNodeHasAInputMessageAttributeCalled_Parent(self):
        self.assertHasAttr( self.metanode._metaNode, "_parent", "The Metanode._metanode node has no _parent attribute.")
        self.assertAttrIsType( self.metanode._metaNode._parent , "message", "The _parent attribute isn't a message type.")

        self.assertAttrIsNotReadable(self.metanode._metaNode._instance, "The _parent attribute should not be readable.")
        self.assertAttrIsWritable(self.metanode._metaNode._instance, "The _parent attribute should be writable.")

    def test_TheMetanodeEncapsulatedUnknownNodeHasAnOutputMessageAttributeCalled_Childs(self):
        self.assertHasAttr( self.metanode._metaNode, "_childs", "The Metanode._metanode node has no _childs attribute.")
        self.assertAttrIsType( self.metanode._metaNode._childs, "message", "The _childs attribute isn't a message type.")

        self.assertAttrIsReadable(self.metanode._metaNode._childs, "The _childs attribute should be readable.")
        self.assertAttrIsNotWritable(self.metanode._metaNode._childs, "The _childs attribute should not be writable.")

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