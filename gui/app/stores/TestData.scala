package stores

import java.io.InputStreamReader

import models.cskg.{Edge, Node}

import scala.collection.mutable

object TestData {
  val edges = deduplicateEdges(readEdges())
  val nodes = deduplicateNodes(readNodes())

  private def deduplicateEdges(edges: List[Edge]): List[Edge] =
    // Default toMap duplicate handling = use later key
    edges.map(edge => ((edge.subject, edge.predicate, edge.`object`), edge)).toMap.values.toList

  private def deduplicateNodes(nodes: List[Node]): List[Node] =
    nodes.map(node => (node.id, node)).toMap.values.toList

  private def readEdges(): List[Edge] = {
    val edgesCsvInputStream = getClass.getResourceAsStream("/test_data/edges.csv")
    try {
      new CskgEdgesCsvReader().read(new InputStreamReader(edgesCsvInputStream)).toList
    } finally {
      edgesCsvInputStream.close()
    }
  }

  private def readNodes(): List[Node] = {
    val nodesCsvInputStream = getClass.getResourceAsStream("/test_data/nodes.csv")
    try {
      new CskgNodesCsvReader().read(new InputStreamReader(nodesCsvInputStream)).toList
    } finally {
      nodesCsvInputStream.close()
    }
  }
}
