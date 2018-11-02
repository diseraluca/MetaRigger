def addDynamicMethod(obj, name, method):
    setattr(obj, name, method)

def composeMayaAttrGetter(node, attrName):
    return lambda : getattr(node, attrName).get()

def composeMayaAttrSetter(node, attrName, **kwargs):
    return lambda value : getattr(node, attrName).set(value, **kwargs)