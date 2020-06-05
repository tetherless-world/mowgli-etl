package stores

import java.io.InputStreamReader

import models.cskg.{Edge, Node}

import scala.collection.mutable

object TestData {
  private val nodesById = deduplicateNodes(readNodes())
  val nodes = nodesById.values.toList
  val edges = removeDanglingEdges(deduplicateEdges(readEdges()), nodesById)

  private def deduplicateEdges(edges: List[Edge]): List[Edge] =
    // Default toMap duplicate handling = use later key
    edges.map(edge => ((edge.subject, edge.predicate, edge.`object`), edge)).toMap.values.toList

  private def deduplicateNodes(nodes: List[Node]): Map[String, Node] =
    nodes.map(node => (node.id, node)).toMap

  private def readEdges(): List[Edge] = {
    val edgesCsvInputStream = getClass.getResourceAsStream("/test_data/edges.csv.bz2")
    try {
      new CskgEdgesCsvReader().readCompressed(edgesCsvInputStream).toList
    } finally {
      edgesCsvInputStream.close()
    }
  }

  private def readNodes(): List[Node] = {
    val nodesCsvInputStream = getClass.getResourceAsStream("/test_data/nodes.csv.bz2")
    try {
      new CskgNodesCsvReader().readCompressed(nodesCsvInputStream).toList
    } finally {
      nodesCsvInputStream.close()
    }
  }

  private def removeDanglingEdges(edges: List[Edge], nodesById: Map[String, Node]): List[Edge] =
    edges.filter(edge => nodesById.contains(edge.subject) && nodesById.contains(edge.`object`))
}
