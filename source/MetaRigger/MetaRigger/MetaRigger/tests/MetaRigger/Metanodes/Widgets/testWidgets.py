import unittest

import pymel.core
import MetaRigger.Metanodes.Widgets.Widget
import MetaRigger.Utils.TestUtils.MetariggerTestCase

class Test_testWidgets(MetaRigger.Utils.TestUtils.MetariggerTestCase.MetariggerTestCase):
    def setUp(self):
        self.Widget = MetaRigger.Metanodes.Widgets.Widget.Widget()

    def test_AWidgetCreatesAnTransformMayaNodeWhenInstanciated(self):
        count = len(pymel.core.ls(type = 'transform'))
        MetaRigger.Metanodes.Widgets.Widget.Widget()

        self.assertEqual(len(pymel.core.ls(type = 'transform')), count + 1, "The Widget did not create a transform node.")

    def test_TheWidgetConstructorRaisesATypeErrorExceptionIfTheTypeArgumentIsntAClassDerivedFromTransform(self):
        self.assertRaises(TypeError, MetaRigger.Metanodes.Widgets.Widget.Widget, type = pymel.core.nodetypes.Unknown)
        self.assertRaises(TypeError, MetaRigger.Metanodes.Widgets.Widget.Widget, type = int)

    def test_TheWidgetBuildMethodSetsTheTranslationOfTheWrappedNodeToThePositionOfItsMayaNodeInstace(self):
        self.Widget._metaNode.setTranslation([10, 100, 1000])
        self.Widget.build()

        self.assertEqual(self.Widget.walkTo_instance().getTranslation(), self.Widget._metaNode.getTranslation(), "The build method did not move the wrapped node to the correct position.")

    def test_TheWidgetBuildMethodSetsTheRotationOfTheWrappedNodeToThatOfItsMayaNodeInstace(self):
        self.Widget._metaNode.setRotation([10, 100, 1000])
        self.Widget.build()

        self.assertTrue(self.Widget.walkTo_instance().getRotation().isEquivalent(self.Widget._metaNode.getRotation()), "The build method did not rotate the wrapped node to the correct position.")

    def test_TheWidgetBuildMethodSetsTheScaleOfTheWrappedNodeToThatOfItsMayaNodeInstace(self):
        self.Widget._metaNode.setScale([10, 100, 1000])
        self.Widget.build()

        self.assertEqual(self.Widget.walkTo_instance().getScale(), self.Widget._metaNode.getScale(), "The build method did not move the wrapped node to the correct position.")

if __name__ == '__main__':
    unittest.main()
