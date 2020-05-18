package stores

import java.io.InputStreamReader

import models.cskg.{Edge, Node}

object TestData {
  val edges = readEdges()
  val nodes = readNodes()

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
