import MetaRigger.Metanodes.Metanode

class Module(MetaRigger.Metanodes.Metanode.Metanode):
    def addNode(self, name, node):
        self.addConnection(name, False)

        self.getPlug(name) >> node.getPlug("_parent")

    def build(self):
        for connection in self.listConnections():
            if self.walkTo(connection) is not None:
                self.walkTo(connection).build()