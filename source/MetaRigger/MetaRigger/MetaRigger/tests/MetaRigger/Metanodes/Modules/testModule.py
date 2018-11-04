import unittest

import pymel.core
import MetaRigger.Metanodes.Modules.Module
import MetaRigger.Utils.TestUtils.MetariggerTestCase

class Test_testModule(MetaRigger.Utils.TestUtils.MetariggerTestCase.MetariggerTestCase):
    def setUp(self):
        self.module = MetaRigger.Metanodes.Modules.Module.Module()

    def test_TheModuleAddNodeMethodAddsAnOutputConnectionToTheModule(self):
        self.module.addNode("Shoulder", MetaRigger.Metanodes.Metanode.Metanode())

        self.assertHasAttr(self.module._metaNode, "Shoulder", "The connection attribute was not added.")
        self.assertAttrIsType(self.module._metaNode.Shoulder, "message", "The attribute was added with the wrong type.")
        self.assertAttrIsReadable(self.module._metaNode.Shoulder, "An output connection should be readable.")
        self.assertAttrIsNotWritable(self.module._metaNode.Shoulder, "An output connection should not be writable.")

    def test_TheModuleAddNodeMehtodConnectsTheNewCnnectionToTheParentConnectionOfThePassedInNode(self):
        node = MetaRigger.Metanodes.Metanode.Metanode()
        self.module.addNode("Shoulder", node)

        self.assertIn(node._metaNode, self.module._metaNode.Shoulder.listConnections(), "The newNode message attribute wasn't connected.")

    def test_TheModuleBuildMethodBuildsEveryNodeThatWasAddedToIt(self):
        nodes = [MetaRigger.Metanodes.Metanode.Metanode() for x in range(0, 5)]
        for index, node in enumerate(nodes):
            self.module.addNode("TestNode_{0}".format(index), node)

        self.module.build()
        for node in nodes:
            self.assertIsNotNone(node.walkTo_instance(), "One or more of the nodes were not built.")

if __name__ == '__main__':
    unittest.main()
