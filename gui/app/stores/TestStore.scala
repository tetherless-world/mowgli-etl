package stores

import java.io.InputStreamReader

import models.cskg.{Edge, Node}

final class TestStore(edges: List[Edge], nodes: List[Node]) extends MemStore(edges, nodes) {
}

object TestStore {
  def apply(): TestStore = {
    val edgesCsvInputStream = getClass.getResourceAsStream("/test_data/edges.csv")
    try {
      val nodesCsvInputStream = getClass.getResourceAsStream("/test_data/nodes.csv")
      try {
        val edges = new CskgEdgesCsvReader().read(new InputStreamReader(edgesCsvInputStream)).toList
        val nodes = new CskgNodesCsvReader().read(new InputStreamReader(nodesCsvInputStream)).toList
        new TestStore(edges, nodes)
      } finally {
        nodesCsvInputStream.close()
      }
    } finally {
      edgesCsvInputStream.close()
    }
  }
}
