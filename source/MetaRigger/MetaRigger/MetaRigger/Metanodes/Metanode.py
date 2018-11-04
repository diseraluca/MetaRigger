import pymel.core
import inspect

import MetaRigger.Utils.DynamicClassesUtils.DynamicMethods as DynamicMethods

class Metanode(object):
    """
    The Metanode class wraps a maya node in the dg graph.

    The Metanode class is the basic building block for a metadata network.
    A metadata network is a network of nodes that runs parallel to a maya node network and
    helps with traversing the graph while storing (meta)data information about its content.
    A metanode class wraps a actual instance of an unknown node in the maya graph.
    The node is used to contain the actual metadata.

    The metanode class provides a few different datatypes to store its data.
        Connections
            Connection are attributes that defines a relationship within the node graph.
            Connection are either input or output attributes.
            Every time a connection with name {name} is added to a metanode a corresponding walkTo{name} method, that returns
            the node that has a relation with the connection, is added.

            A Metanode class instance by default provides three connections : _parent(input), _childs(output) and _instance(input)

        Options
            Options are attributes that defines the On/Off statuses to be used for branching in the building process.
            Every time an option is added with name {name} two corresponding methods are added.
            The is{name} method which return the current status of the option.
            The set{name} method which sets the option on or off.

        Counters
            Counters are attributes that are used to store variable amounts of something.
            Every couunter has a closed interval of values that it supports.
            Every time a counter is added with name {name}, two corresponding methods are added:
            An howMany{name}, which retrieves the value stored in the counter and
            a setHowMany{name}, which stores a new value into the counter.

            If a value outside the supported interval is setted on the counter, the value
            is clamped to the nearest supported amount.

        Informations
            Informations are attribute that are used to store generic, string form, values.
            They should be used every time an important piece of data does not fit in another datatype.
            Every time an information is added with name {name}, two correlated methods are added to the Metanode Class Instance:
            The which{name} method which is a getter for the new Information and
            The setWhich{name} method which is a setter for the new Information.

    Attributes:
        _metaNode : Contains a reference to the actual metanode instance in the graph
        _type : Contains the class, derived from pymel.core.general.PyNode, that the node is supposed to wrap.
        _connections : A list of names of the added connections

    Methods:
        build() : Builds the actual node that is wrapped by the Metanode instance
        addConnection(name, isInput = True) : Adds a new connection to the metanode
        walkTo(connection) : Returns the node at the end of the connection
        addOption(name, default) : Adds a new option to the metanode
        addCounter(name, default, min, max)  : Adds a new counter to the metanode
        getPlug() : Retrieves a plug from the metanode maya instance
        listConnections() : Retrieves a list of the added connections' names
    """

    def __init__(self, type=pymel.core.nodetypes.Unknown):
        """
        Initialises the Metanode. 
        
        A few things happens when a Metanode is initialized.
        Firstly, a new Unknown node is created in the maya scene and a reference to it is stored in the Metanode class instance.
        Then the passed in type, which should be a class derived from pymel.core.general.PyNode, is stored inside the Metanode class instance.
        After this the preInitialization of the class is run to set up the actual metanode instance in the maya scene and the Metanode class instance.

        If a non-class or a class that isn't derived from pymel.core.general.PyNode is passed as the type parameter a TypeError is raised. 

        Arguments:
            type : A class, derived from pymel.core.general.PyNode, that represents the type of the node that is wrapped by this Metanode class instance.

        Raise:
            TypeError : Raised when the type parameter is passed has a non-class or a class that isn't derived from pymel.core.general.PyNode.
        """

        super(Metanode, self).__init__()
        if (not inspect.isclass(type) or not issubclass(type, pymel.core.general.PyNode)):
           raise TypeError

        self._metaNode = self._buildMetanode()
        self._type = type
        self._connections = []

        self._preInitialization()

    def _buildMetanode(self):
        """
        Builds the actual maya node representation of this metanode.

        This method should be overriden by child classes that are represented with a
        node that isn't of type Unknown.

        Returns:
            An instance of the type of node that is used to represent the Metanode in the maya graph.
        """

        return  pymel.core.nodetypes.Unknown()

    def _preInitialization(self):
        """
        Performs the needed setUp for the Metanode class instance and the metanode actual node instance.

        During pre-initialization a series of attributes are added to the metanode instance that mirrors some of the data stored by
        the metanode plus the attribute needed to connect the metanode with other metanodes to create a network.

        After pre-initialization you can expect to have the following attributes of the metanode instance :
            - _type -> string
            - _instance -> message ( Not Readable )
            - _parent -> message ( Not Readable )
            - _childs -> message ( Not Writable )

        Furthermore you can expect to have the following methods:
            which_type()
            setWhich_type()
            walkTo_instance()
            is_instanceConnected()
            walkTo_parent()
            is_parentConnected()
            walkTo_childs()
            is_childsConnected()

        These attributes can be used to reconstruct a Metanode class instance from an actual metanode.
        Furthermore, the _parent and _childs attribute connections are used to represent relationships in a metanode network.
        
        The _instance attribute is used to store a connection to the actual instance  of the node wrapped by this metanode, if already built.
        """

        self.addInformation("_type")
        self._addUntrackedConnection("_instance")
        self._addUntrackedConnection("_parent")
        self._addUntrackedConnection("_childs", False)

    def build(self):
        """
        Builds the actual node that is wrapped by this metanode.
        
        A default instance of a node of type self._type is created if it wasn't already previously built.

        Returns:
            A reference to the node wrapped by this metanode.
        """

        if not self.is_instanceConnected() :
           self._type().message >> self._metaNode._instance

        return self.walkTo_instance()

    def addConnection(self, name, isInput = True):
        """
        Adds a new connection to the metanode

        A connection is a message attribute, either not readable or not writable, that serves the purpose of
        representing a relationship with other nodes.
        Every time a connection is added with name {name}, a related walkTo{name} method is added 
        to the Metanode class instance.
        This method returns the node the connection points to.
        A is{name}Connected method is added too and returns a boolean indication whether the node has any
        connection.

        Arguments:
            name : The name of the connection
            isInput : Declares the connection as an input attribute if True and as an Output Attribute if False
        """

        self._addUntrackedConnection(name, isInput)
        self._connections.append(name)

    def _addUntrackedConnection(self, name, isInput = True):
        """
        Adds a connection without storing its names in the metanode _connections member.

        This is done to distinguish between user defined connections and default connections.
        Every default connection is untracked and should not appear in any connection list on the metanode.
        
        This is for internal use only.

        Arguments:
            name : The name of the connection
            isInput : Declares the connection as an input attribute if True and as an Output Attribute if False
        """

        self._metaNode.addAttr(name, attributeType = "message", writable = isInput, readable = not isInput)

        DynamicMethods.addDynamicMethod(self, "walkTo{0}".format(name), self._composeWalkToAttr(name))
        DynamicMethods.addDynamicMethod(self, "is{0}Connected".format(name), lambda : getattr(self._metaNode, name).isConnected())

    def walkTo(self, connection):
        """
        Returns the node that is at the end of connection

        If the connection has no current relationship this method returns None.
        If an output connections has multiple relationships the one that was formed first is returned.

        Arguments:
            connection : The name of the connection to walk

        Returns:
            Returns either a pymel.core.general.PyNode derived class or None
        """

        connectedNodes = pymel.core.listConnections(getattr(self._metaNode, connection).name())
        if (connectedNodes):
            return connectedNodes[-1]
        return None

    def _composeWalkToAttr(self, connection):
        """
        Composes the walk function for connections.

        This private method is used, internally, to create the walkTo methods when a connection is added.
        
        Arguments:
            connection : The connection we are creating the method for

        Returns:
            A closure that walks the desired connection
        """

        def walkToAttr():
            return self.walkTo(connection)
        return walkToAttr

    def addOption(self, name, default = True):
        """
        Add an option attribute to the Metanode instance.

        An option is a boolean attribute that serves the purpose of providing an easy way to turn
        features on or off.
        Every time an option with name as {name} is added, two methods are added to the Metanode class instance:
        is{name}, which returns the current status of the option and
        set{name}, which sets the option either on or off.

        Arguments:
            name : The name of the option
            default : The initial ( boolean ) value of the option.
        """

        self._metaNode.addAttr(name, attributeType = "bool", defaultValue = default);

        DynamicMethods.addDynamicMethod(self, "is{0}".format(name), DynamicMethods.composeMayaAttrGetter(self._metaNode, name) )
        DynamicMethods.addDynamicMethod(self, "set{0}".format(name), DynamicMethods.composeMayaAttrSetter(self._metaNode, name) )

    def addCounter(self, name, default = 0.0, min = 0.0, max = 1.0):
        """
        Adds a counter attribute to the Metanode instance.

        A counter is a float attribute that serves the purpose of keeping the count of variable build parameters
        and enables their customizations.
        It can be used, for example, to set the number of joints in a spine module.

        Every time a counter is added with name as {name}, two methods are added to the Metanode class instance:
        howMany{name}, which returns the value stored in the counter and
        setHowMany{name}, which sets the value stored in counter. If the value that is setted is outside the
        minum and maximum range of the counter the value is clamped to the nearest valid amount.

        Arguments:
            name : The name of the counter
            default : The initial (float) value of the counter
            min : The minimun acceptable value for the counter
            max : The maximum acceptable value for the counter
        """

        self._metaNode.addAttr(name, attributeType = "float", defaultValue = default, min = min, max = max)

        DynamicMethods.addDynamicMethod(self, "howMany{0}".format(name), DynamicMethods.composeMayaAttrGetter(self._metaNode, name) )
        DynamicMethods.addDynamicMethod(self, "setHowMany{0}".format(name), DynamicMethods.composeMayaAttrSetter(self._metaNode, name, clamp = True) )

    def addInformation(self, name):
        """
        Adds an Information attribute to the Metanode Instance.

        An information is a string attribute that is used to store general informations that don't fit in other attributes.
        Every time an information is added with name as {name}, two methods are added to the Metanode class Instance:
        which{name}, which will return the value stored in the information and
        setWhich{name}, which sets the value of the information.

        Arguments:
            name : The name of the information
        """

        self._metaNode.addAttr(name, dataType = "string")

        DynamicMethods.addDynamicMethod(self, "which{0}".format(name), DynamicMethods.composeMayaAttrGetter(self._metaNode, name) )
        DynamicMethods.addDynamicMethod(self, "setWhich{0}".format(name), DynamicMethods.composeMayaAttrSetter(self._metaNode, name) )

    def getPlug(self, attrName):
        """
        Retrieves a plug from the metanode maya instance.

        Returns None if the plug can't be found.

        Arguments:
            attrName : The name of the plug to retrieve

        Returns:
            The searched for flag or None
        """

        return getattr(self._metaNode, attrName, None)

    def listConnections(self):
        """
        Return a list of all the added connections.

        Returns:
            The list of added connections
        """

        return self._connections