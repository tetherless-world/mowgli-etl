package stores

import models.cskg.{Edge, Node}

class MemStore(val edges: List[Edge], val nodes: List[Node]) extends Store {
  final override def getEdgesByObject(objectNodeId: String): List[Edge] =
    edges.filter(edge => edge.`object` == objectNodeId)

  final override def getEdgesBySubject(subjectNodeId: String): List[Edge] =
    edges.filter(edge => edge.subject == subjectNodeId)

  final override def getNodeById(id: String): Option[Node] =
    nodes.find(node => node.id == id)

  final override def getMatchingNodes(limit: Int, offset: Int, text: String): List[Node] =
    nodes.filter(node => node.label.contains(text)).drop(offset).take(limit)

  final override def getMatchingNodesCount(text: String): Int =
    getMatchingNodes(limit = Integer.MAX_VALUE, offset = 0, text = text).size
}
