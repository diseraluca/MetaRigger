import unittest
import inspect

import pymel.core

class MetariggerTestCase(unittest.TestCase):
    """A class that encapsulate some utility methods and asserts for the testing of this project."""

    def assertIsClass(self, obj, msg = ""):
        """
        Checks if something is a class.

        Arguments:
            obj : The object or variable to check
            msg : A message to print in case of failure
        """

        self.assertTrue( inspect.isclass(obj), msg)

    def assertIsSubClass(self, obj, cls, msg = ""):
        """
        Checks if something is a subclass of another class.

        Arguments:
            obj : The object or variable to check
            msg : A message to print in case of failure
        """

        self.assertTrue( issubclass(obj, cls), msg)

    def assertHasMethod(self, obj, method, msg = ""):
        """
        Checks if an object has a method.

        Arguments:
            obj : The object to check
            method : The name of the method
        """

        self.assertTrue(hasattr(obj, method), msg)

    def assertNotHasMethod(self, obj, method, msg = ""):
        """
        Checks that an object does not have a method.

        Arguments:
            obj : The object to check
            method : The name of the method
        """

        self.assertFalse(hasattr(obj, method), msg)

    def assertHasAttr(self, node, attr, msg = ""):
        """
        Checks if a maya node has an attribute.

        Arguments:
            node : A pymel class representing the node
            attr : The name of the attribute to check
            msg : A message to print in case of failure
        """

        self.assertTrue( node.hasAttr(attr), msg)

    def assertNotHasAttr(self, node, attr, msg = ""):
        """
        Checks that a maya node doesn't have an attribute.

        Arguments:
            node : A pymel class representing the node
            attr : The name of the attribute to check
            msg : A message to print in case of failure
        """

        self.assertFalse( node.hasAttr(attr), msg)

    def assertAttrIsType(self, attr, type, msg = ""):
        """
        Checks if a maya node attribute is of a certain type.

        Arguments:
            attr : The name of the attribute to check
            type : The type the attribute should be
            msg : A message to print in case of failure
        """

        self.assertEquals( attr.type() , type, msg)

    def assertAttrIsReadable(self, attr, msg):
        """
        Checks if a maya node attribute is readable.

        Arguments:
            attr : The name of the attribute to check
            msg : A message to print in case of failure
        """

        self.assertTrue(pymel.core.general.attributeQuery( attr.attrName(), node = attr.node().name(), readable = True), msg)

    def assertAttrIsNotReadable(self, attr, msg):
        """
        Checks if a maya node attribute is not readable.

        Arguments:
            attr : The name of the attribute to check
            msg : A message to print in case of failure
        """

        self.assertFalse(pymel.core.general.attributeQuery( attr.attrName(), node = attr.node().name(), readable = True), msg)


    def assertAttrIsWritable(self, attr, msg):
        """
        Checks if a maya node attribute is writable.

        Arguments:
            attr : The name of the attribute to check
            msg : A message to print in case of failure
        """

        self.assertTrue(pymel.core.general.attributeQuery( attr.attrName(), node = attr.node().name(), writable = True), msg)

    def assertAttrIsNotWritable(self, attr, msg):
        """
        Checks if a maya node attribute is not writable.

        Arguments:
            attr : The name of the attribute to check
            msg : A message to print in case of failure
        """

        self.assertFalse(pymel.core.general.attributeQuery( attr.attrName(), node = attr.node().name(), writable = True), msg)