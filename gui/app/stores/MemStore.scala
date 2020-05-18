package stores

import models.cskg.{Edge, Node}

class MemStore(val edges: List[Edge], val nodes: List[Node]) extends Store {
  override def getEdgesBySubject(subjectNodeId: String): List[Edge] =
    edges.filter(edge => edge.subject == subjectNodeId)

  override def getNodeById(id: String): Node =
    nodes.find(node => node.id == id).getOrElse(throw new NoSuchElementException)
}
