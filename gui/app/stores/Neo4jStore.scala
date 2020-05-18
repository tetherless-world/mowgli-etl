package stores
import models.cskg.{Edge, Node}

class Neo4jStore extends Store {
  override def getEdgesBySubject(subjectNodeId: String): List[Edge] = throw new UnsupportedOperationException

  override def getNodeById(id: String): Node = throw new UnsupportedOperationException
}
