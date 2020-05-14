package stores
import models.cskg.{Edge, Node}

class PlaceholderStore extends Store {
  override def getEdgesBySubject(subjectNodeId: String): List[Edge] = throw new UnsupportedOperationException

  override def getNodeById(id: String): Node = throw new UnsupportedOperationException
}
