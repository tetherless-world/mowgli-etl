package stores

import com.google.inject.ImplementedBy
import models.cskg.{Edge, Node}

@ImplementedBy(classOf[Neo4jStore])
trait Store {
  /**
   * Get all of the edges that have the given node ID as a subject.
   */
  def getEdgesBySubject(subjectNodeId: String): List[Edge]

  /**
   * Get a node by ID.
   */
  def getNodeById(id: String): Node

  /**
   * Fulltext search nodes.
   */
  def searchNodes(limit: Int, offset: Int, text: String): List[Node]
}
