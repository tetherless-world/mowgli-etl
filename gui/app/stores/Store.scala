package stores

import com.google.inject.ImplementedBy
import models.cskg.{Edge, Node}

@ImplementedBy(classOf[PlaceholderStore])
trait Store {
  def getEdgesBySubject(subjectNodeId: String): List[Edge]
  def getNodeById(id: String): Node
}
