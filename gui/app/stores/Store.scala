package stores

import com.google.inject.ImplementedBy
import models.cskg.{Edge, Node}

@ImplementedBy(classOf[Neo4jStore])
trait Store {
  def getEdgesBySubject(subjectNodeId: String): List[Edge]
  def getNodeById(id: String): Node
}
