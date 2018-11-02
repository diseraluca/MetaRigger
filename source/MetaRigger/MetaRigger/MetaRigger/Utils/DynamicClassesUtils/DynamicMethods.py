def addDynamicMethod(obj, name, method):
    """
    Adds a method on the object.

    Arguments:
        obj : The object on which to add the method
        name : The name the method should have on the object
        method : The function to add as a method
    """

    setattr(obj, name, method)

def composeMayaAttrGetter(node, attrName):
    """
    Creates a function to get an attribute from a maya node.

    Arguments:
        node : The node wich own the attribute
        attrName : The name of the attribute to retrieve

    Returns:
        A function that gets the value of the attribute on the node.
    """

    return lambda : getattr(node, attrName).get()

def composeMayaAttrSetter(node, attrName, **kwargs):
    """
    Creates a function to set an attribute from a maya node.

    Arguments:
        node : The node which owns the attribute
        attrName : The name of the attribute to set
        **kwargs : Named arguments to pass to the setter of the attribute.
                   They should be valid flags from maya setAttr command.

    Returns:
        A function that sets the value of the attribute on the node.
    """

    return lambda value : getattr(node, attrName).set(value, **kwargs)