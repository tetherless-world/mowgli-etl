package stores

import models.cskg.{Edge, Node}

class MemStore(val edges: List[Edge], val nodes: List[Node]) extends Store {
  final override def getEdgesBySubject(subjectNodeId: String): List[Edge] =
    edges.filter(edge => edge.subject == subjectNodeId)

  final override def getNodeById(id: String): Node =
    nodes.find(node => node.id == id).getOrElse(throw new NoSuchElementException)

  final override def searchNodes(limit: Int, offset: Int, text: String): List[Node] =
    nodes.filter(node => node.label.contains(text)).drop(offset).take(limit)
}
