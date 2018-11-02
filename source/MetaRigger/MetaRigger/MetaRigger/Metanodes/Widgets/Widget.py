import inspect

import pymel.core
import MetaRigger.Metanodes.Metanode

class Widget(MetaRigger.Metanodes.Metanode.Metanode):
    """
    Widgets are Metanodes that are represented by a Dag node in the Maya scene and Wraps DAG nodes only.

    Widgets provide a way to visually customize the positional values of a Metanode before its build method gets called.
    This is useful to provide a way to customize Modules and adjust them to different meshes.
    """

    def __init__(self, type = pymel.core.nodetypes.Transform):
        """
        Initializes the Widget.

        Widgets are initialized like any other Metanode but their Maya graph representation is
        that of a Transform derived node and they wrap only nodes that are derived from this class.

        If a type that isn't derived from pymel.core.nodetypes.Transform is passed as the type for the Widget constructor
        a TypeError is raised.

        Arguments:
            type : The type of the node that is wrapped by this widget. Only Transform derived nodes are accepted.

        Raises:
            TypeError
        """

        if (not inspect.isclass(type) or not issubclass(type, pymel.core.nodetypes.Transform)):
           raise TypeError

        return super(Widget, self).__init__(type)

    def _buildMetanode(self):
        """
        Overloaded to set the Maya Representation node type to pymel.core.nodetypes.Transform.

        Returns:
            A pymel.core.nodetypes.Trasform instance
        """

        return pymel.core.nodetypes.Transform()

    def build(self):
        """
        Builds the node wrapped by this widget.

        A Widget built node is created like any other Metanode wrapped node.
        Furthermore, the position, rotation and scale of the newly created node is set to that of
        the Metanode Maya Node representation.

        Returns:
            The node that is wrapped by this Widget.
        """

        super(Widget, self).build()
        self.walkTo_instance().setTranslation(self._metaNode.getTranslation())
        self.walkTo_instance().setRotation(self._metaNode.getRotation())
        self.walkTo_instance().setScale(self._metaNode.getScale())

        return self.walkTo_instance()